#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use DBI;
use HTML::Entities;

# new cgi query
my $q = new CGI;
# fetching cookie
my $ssid = $q->cookie('MYCOPYPASTACOOKIE');
# printing header
print $q->header;
# login error or not
my $err = 0;

sub  trim { 
	my $s = shift;
	$s =~ s/^\s+|\s+$//g;
	return $s;
}

# proper logged in?
my $login = 0;

if($ssid eq "") {
	# empty/no cookie found. Hence not logged in
} else {
	# cookie has some value, hence loading session from $ssid
	$session = CGI::Session->load($ssid) or die "$!";
	if($session->is_expired || $session->is_empty) {
		# if session is expired/empty, need to relogin
	} else {
		my $value = $session->param('logged_in_status_mycp');
		if ($value eq "1") {
			# properly logged in
			$login = 1;
		}
	}
}

if ($login == 0) {
	my $url="login.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
} else {

	my $profileid = $q->param('id');
	
	if ($profileid eq "") {
		$profileid = $session->param('logged_in_userid_mycp');
	}
	
	my $message = "";
	
	if ($session->param('logged_in_userid_mycp') eq $profileid) {
		$message = "(Current User) <a class=\"edit_button\" href=\"editprofile.cgi?id=$profileid\"><img src=\"images/edit.jpg\" alt=\"Edit\" style=\"width:10px;height:10px;padding-right:3px\">Edit</a>";
	}
	
	print '<html lang="en-US">
		<head>
			<title>My Copy-Pasta</title>
			<link rel="shortcut icon" href="images/newlogo.ico">
			<link rel="stylesheet" type="text/css" href="css/style.css">
			<link rel="stylesheet" type="text/css" href="css/viewstyle.css">
			<link rel="stylesheet" type="text/css" href="css/registerpasta.css">
			<link rel="stylesheet" type="text/css" href="css/addpasta.css">
			<div id="fb-root"></div>
			<script>(function(d, s, id) {
				  var js, fjs = d.getElementsByTagName(s)[0];
				  if (d.getElementById(id)) return;
				  js = d.createElement(s); js.id = id;
				  js.src = "//connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v2.4&appId=173510282674533";
				  fjs.parentNode.insertBefore(js, fjs);
				}(document, \'script\', \'facebook-jssdk\'));
			</script>
		</head>
		
		<body>
			<table class="box" align="center" width="65%">
				<tr>
					<td>
						<div style="text-align:center"><img src="images/banner.jpg" alt="Edit" style="width:100%;height:250px;"></div>
					</td>
				</tr>
				<tr>
					<td>
					    <div id="centeredmenu">
					      <ul>
					        <li><a href="index.cgi">Home</a></li>';
					        if ($login) {
						        print '<li><a href="addpasta.cgi">Add Copy-Pasta</a></li>';
					        }
					        print '<li><a href="view.cgi">My Copy-Pasta</a></li>
					        <li><a href="tutorial.cgi">Tutorials</a></li>
					        <li><a href="search.cgi">Search Copy-Pasta</a></li>
					        <li><a href="contact.cgi">Contact Us</a></li>';
					        if ($login) {
					        	my $getuser = $session->param('logged_in_userid_mycp');
						        print '<li><a href="logout.cgi">Logout</a></li>';
						        print "<li><a href=\"profile.cgi?id=$getuser\">Profile</a></li>";
					        } else {
					        	print '<li><a href="login.cgi">Login</a></li>';
					        }
					      print '</ul>
					    </div>
					</td>
				</tr>';
				
				my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
				my $dbh = DBI->connect($dsn,"root","");
				my $sth = $dbh->prepare("SELECT myusername,mydob,name,displaypic,registereddate,myemail,myprofession,myplace,activeaccount,admin FROM userdatabase where id='$profileid' and deleted=0");
				$sth->execute();
				my $countres = $sth->rows;
				if ($countres == 0) {
					print "<tr><td><font color=\"red\">No Pofile Found.</font></td></tr></table>";
				} else {
					my $name = "";
					my $myusername = "";
					my $displaypic = "";
					my $registereddate = "";
					my $myemail = "";
					my $myprofession = "";
					my $myplace = "";
					my $activeaccount = "";
					my $admin = "";
					my $mydob = "";
					while (my $ref = $sth->fetchrow_hashref()) {
						$myusername = $ref->{'myusername'};
						$name = $ref->{'name'};
						$displaypic = $ref->{'displaypic'};
						$registereddate = $ref->{'registereddate'};
						$myemail = $ref->{'myemail'};
						$myprofession = $ref->{'myprofession'};
						$myplace = $ref->{'myplace'};
						$activeaccount = $ref->{'activeaccount'};
						$admin = $ref->{'admin'};
						$mydob = $ref->{'mydob'};
						break;
					}
					$sth->finish();
					$dbh->disconnect();
					my $account = "";
					if ($admin == 0) {
						$account = "guest account";
					} elsif ($admin == 1) {
						$account = "admin account";
					} else {
						$account = "normal user account";
					}
					
					my $acntstate = "";
					my $acntcol = "white";
					
					if ($activeaccount == 0) {
						$acntstate = "Inactive Account";
						$acntcol = "red";
					} else {
						$acntstate = "Active Account";
						$acntcol = "green";
					}
					
					
					
					print "</table><section class=\"registerdata\">
					<div class=\"loginbox\">Copy-Pasta Profile of <font color=black>$name</font> $message</div>
					<div class='container2'>
						<div>
							<img width=\"120px\" alt=\"$myusername\" border=\"2\" class='iconDetails' src=\"get_blob.cgi?id=$profileid\">
			    		</div>	
						<div style='margin-left:60px;'>
		    				<form>
								<text class=\"fontdec\">Username</text>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%\" value=\"$myusername\" readonly><br /><br />
				    			
				    			<text class=\"fontdec\">Name</text>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%\" value=\"$name\" readonly><br /><br />
				    			
				    			<text class=\"fontdec\">Email</text>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%\" value=\"$myemail\" readonly><br /><br />
				    			
				    			<text class=\"fontdec\">Date of Birth</text>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%\" value=\"$mydob\" readonly><br /><br />
				    			
				    			<text class=\"fontdec\">Occupation</text>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%\" value=\"$myprofession\" readonly><br /><br />
				    			
				    			<text class=\"fontdec\">Place</text>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%\" value=\"$myplace\" readonly><br /><br />
				    			
				    			<text class=\"fontdec\">Account Reg. Date</text>
				    				&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%\" value=\"$registereddate\" readonly><br /><br />
				    			
				    			<text class=\"fontdec\">Account Type</text>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%\" value=\"$account\" readonly><br /><br />
				    			
				    			<text class=\"fontdec\">Account State</text>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%;background:$acntcol\" value=\"$acntstate\" readonly><br /><br />
				    			
				    			<text class=\"fontdec\">Update Password</text>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<a href=\"updatepassword.cgi?id=$profileid\" class=\"button\">Click to update password</a><br /><br />";
				    			
				    			if ($account eq "admin account") {
					    			print "<text class=\"fontdec\">Pending Account Activations</text>
					    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					    			<a href=\"activateaccount.cgi\" class=\"button\">Click for Pending Account Activations</a><br /><br />";
				    			}
				    			if ($session->param('logged_in_user_mycp') eq "admin" && $session->param('logged_in_userid_mycp') ne $profileid) {
					    			print "<text class=\"fontdec\">Deactivate this account</text>
						    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
						    			<a href=\"deactivateaccount.cgi?id=$profileid\" class=\"button\">Deactivate this account</a><br /><br />";
				    			}
				    			
				    			print "</form>
				    		</div>
						</div>
		    			</section>";
		    			$sth = $dbh->prepare("SELECT category,count FROM categoryinfo where userid='$profileid'");
						$sth->execute();
						print "</table><section class=\"registerdata\">
							<div class=\"loginbox\">Total Category Inputs</div><form>";
							
		    			while (my $ref = $sth->fetchrow_hashref()) {
		    				my $string = "categoryview.cgi?showmycategory=$ref->{'category'}";
							encode_entities($string);
		    				print "<a href =\"$string\"><text class=\"fontdec\">$ref->{'category'}</text></a>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%\" value=\"$ref->{'count'}\" readonly><br /><br />";
						}
		    			print "</form>
				    		</div>
						</div>
		    			</section>";
		    			
		    			$sth = $dbh->prepare("SELECT tag,tagcount FROM taginfo where userid='$profileid'");
						$sth->execute();
						print "<section class=\"registerdata\">
							<div class=\"loginbox\">Total Tag Inputs</div><form>";
							
		    			while (my $ref = $sth->fetchrow_hashref()) {
		    				$val = trim($ref->{'tag'});
							my $string = "tagview.cgi?showmytag=$val";
	   						encode_entities($string);
		    				print "<a href =\"$string\"><text class=\"fontdec\">$ref->{'tag'}</text></a>
				    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				    			<input type=\"text\" style=\"width:60%\" value=\"$ref->{'tagcount'}\" readonly><br /><br />";
						}
		    			print "</form>
				    		</div>
						</div>
		    			</section>";
				}
				$sth->finish();
				$dbh->disconnect();
			print '</body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';
}

1;