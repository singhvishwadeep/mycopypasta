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
				my $sth = $dbh->prepare("SELECT myusername,mydob,name,displaypic,registereddate,myemail,myprofession,myplace,activeaccount,admin,registeredip,http_agent FROM userdatabase where id='$profileid' and deleted=0");
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
					my $regip = "";
					my $http = "";
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
						$regip = $ref->{'registeredip'};
						$http = $ref->{'http_agent'};
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
		    					<table>
								<tr><td><text class=\"fontdec\">Username</text></td>
				    			<td><input type=\"text\" style=\"width:100%\" value=\"$myusername\" readonly></td></tr>
				    			
				    			<tr><td><text class=\"fontdec\">Name</text></td>
				    			<td><input type=\"text\" style=\"width:100%\" value=\"$name\" readonly></td></tr>
				    			
				    			<tr><td><text class=\"fontdec\">Email</text></td>
				    			<td><input type=\"text\" style=\"width:100%\" value=\"$myemail\" readonly></td></tr>
				    			
				    			<tr><td><text class=\"fontdec\">Date of Birth</text></td>
				    			<td><input type=\"text\" style=\"width:100%\" value=\"$mydob\" readonly></td></tr>
				    			
				    			<tr><td><text class=\"fontdec\">Occupation</text></td>
				    			<td><input type=\"text\" style=\"width:100%\" value=\"$myprofession\" readonly></td></tr>
				    			
				    			<tr><td><text class=\"fontdec\">Place</text></td>
				    			<td><input type=\"text\" style=\"width:100%\" value=\"$myplace\" readonly></td></tr>
				    			
				    			<tr><td><text class=\"fontdec\">Account Reg. Date</text></td>
				    			<td><input type=\"text\" style=\"width:100%\" value=\"$registereddate\" readonly></td></tr>
				    			
				    			<tr><td><text class=\"fontdec\">Account Type</text></td>
				    			<td><input type=\"text\" style=\"width:100%\" value=\"$account\" readonly></td></tr>
				    			
				    			<tr><td><text class=\"fontdec\">Account State</text></td>
				    			<td><input type=\"text\" style=\"width:100%;background:$acntcol\" value=\"$acntstate\" readonly></td></tr>
				    			
				    			<tr><td><text class=\"fontdec\">Update Password</text></td>
				    			<td><a href=\"updatepassword.cgi?id=$profileid\" class=\"button\">Click to update password</a></td></tr>";
				    			
				    			if ($session->param('logged_in_user_mycp') eq "admin") {
				    				print "<tr><td><text class=\"fontdec\">Registered IP</text></td>
					    			<td><a href=\"http://www.ip-tracker.org/locator/ip-lookup.php?ip=$regip\" target=\"_blank\">$regip</a></td></tr>";
					    			
					    			print "<tr><td><text class=\"fontdec\">Registered Agent</text></td>
					    			<td><a href=\"http://www.ip-tracker.org/locator/ip-lookup.php?ip=$regip\" target=\"_blank\">$regip</a></td></tr>";
				    			}
				    			
				    			if ($session->param('logged_in_user_mycp') eq "admin" && $myusername eq "admin") {
					    			print "<tr><td><text class=\"fontdec\">Account Activations</text></td>
					    			<td><a href=\"activateaccount.cgi\" class=\"button\">Click for Pending Activations</a></td></tr>";
				    			}
				    			if ($session->param('logged_in_user_mycp') eq "admin" && $myusername ne "admin") {
					    			print "<tr><td><text class=\"fontdec\">Deactivate account</text></td>
						    			<td><input type=\"text\" style=\"width:100%;\" value=\"$http\" readonly></td></tr>";
				    			}
				    			
				    			print "</table></form>
				    		</div>
						</div>
		    			</section>";
		    			$sth = $dbh->prepare("SELECT category,count FROM categoryinfo where userid='$profileid'");
						$sth->execute();
						print "<section class=\"registerdata\">
							<div class=\"loginbox\">Your total Category Inputs</div><form><table>";
							
		    			while (my $ref = $sth->fetchrow_hashref()) {
		    				my $string = "categoryview.cgi?showmycategory=$ref->{'category'}";
							encode_entities($string);
		    				print "<tr><td><a href =\"$string\"><text class=\"fontdec\">$ref->{'category'}</text></a></td>
				    			<td><input type=\"text\" style=\"width:100%\" value=\"$ref->{'count'}\" readonly></td></tr>";
						}
		    			print "</table></form>
				    		</div>
						</div>
		    			</section>";
		    			
		    			$sth = $dbh->prepare("SELECT tag,tagcount FROM taginfo where userid='$profileid'");
						$sth->execute();
						print "<section class=\"registerdata\">
							<div class=\"loginbox\">Your total Tag Inputs</div><form><table>";
							
		    			while (my $ref = $sth->fetchrow_hashref()) {
		    				$val = trim($ref->{'tag'});
							my $string = "tagview.cgi?showmytag=$val";
	   						encode_entities($string);
		    				print "<tr><td><a href =\"$string\"><text class=\"fontdec\">$ref->{'tag'}</text></a></td>
				    			<td><input type=\"text\" style=\"width:100%\" value=\"$ref->{'tagcount'}\" readonly></td></tr>";
						}
		    			print "</table></form>
				    		</div>
						</div>
		    			</section>";
		    			
		    			
		    			if ($session->param('logged_in_user_mycp') eq "admin" || $myusername eq $session->param('logged_in_user_mycp')) {
			    			$sth = $dbh->prepare("SELECT ip,http_agent,date FROM login_ip_track where userid='$profileid' AND username='$myusername' LIMIT 20");
							$sth->execute();
							print "<section class=\"registerdata\">
								<div class=\"loginbox\">Your Last 20 Login Sessions</div><form><table border=\"1\">";
								print "<tr>
			    						<td>S.No.</td>
			    						<td>date</td>
			    						<td>IP</td>
			    						<td>HTTP_USER_AGENT</td>
			    						</tr>";
							my $i = 0;
			    			while (my $ref = $sth->fetchrow_hashref()) {
			    				$i++;
			    				$val = trim($ref->{'tag'});
								my $string = "tagview.cgi?showmytag=$val";
		   						encode_entities($string);
			    				print "<tr>
			    						<td>$i</td>
			    						<td>$ref->{'date'}</td>
			    						<td><a href=\"http://www.ip-tracker.org/locator/ip-lookup.php?ip=$ref->{'ip'}\" target=\"_blank\">$ref->{'ip'}</a></td>
			    						<td>$ref->{'http_agent'}</td>
			    						</tr>";
							}
			    			print "</table></form>
					    		</div>
							</div>
			    			</section>";
		    			}
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