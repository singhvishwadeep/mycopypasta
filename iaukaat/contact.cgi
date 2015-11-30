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

print '<html lang="en-US">
	<head>
		<title>My iAukaat</title>
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
					        print '<li><a href="addtransaction.cgi">Add Transaction</a></li>';
				        }
				        print '<li><a href="view.cgi">Show iAukaat</a></li>
				        <li><a href="tutorial.cgi">iAukaat Tutorials</a></li>';
				        if ($login) {
				        	my $getuser = $session->param('logged_in_userid_mycp');
					        print '<li><a href="search.cgi">Search Transactions</a></li>';
					        print '<li><a href="logout.cgi">Logout</a></li>';
					        print "<li><a href=\"profile.cgi?id=$getuser\">My Profile</a></li>";
				        } else {
				        	print '<li><a href="login.cgi">Login</a></li>';
				        }
				      print '<li><a href="contact.cgi">Contact iAukaat Team</a></li></ul>
				    </div>
				</td>
			</tr>
		<tr><td>
		
		
		<div class=\'container2\'>
			<div>
				<img width="440px" alt="My iAukaat" border="2" class=\'iconDetails_contact\' src="images/show.jpg">
    		</div>	
			<div style=\'margin-left:60px;text-align: justify;\'>
				<text class="fontdec" style="padding:10px;"><font size="6">Let&#39;s get Together</font></text><br>
				<p><text class="fontdec" style="padding:10px;">Hello,</text><br></p>
				<p><text class="fontdec" style="padding:10px;">Myself Vishwadeep Singh (M/29), working in reputed IT company as System Software Engineer II and trying to 
				figure out different dimensions to solve different problems.</text></p>
				
				<p><text class="fontdec" style="padding:10px;">We are here to answer any question you may have about iAukaat experiences.
				Reach out to us, and we will respond as soon as possible.</text></p>
				<p><text class="fontdec" style="padding:10px;">Even if there is something you have always wanted to experience and can&#39;t find it on combadi, let us know and we 
				promise we&#39;ll do our best to find it for you and send you there.</text></p>
				<p><text class="fontdec" style="padding:10px;">Contact Us: </text><a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a></p>
			</div>
		</div>
		
		</td>
		
		</tr>
		</table>';
		my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
		my $dbh = DBI->connect($dsn,"root","");
		$sth = $dbh->prepare("SELECT category,count FROM categoryinfo");
		$sth->execute();
		print "</table><section class=\"registerdata\">
						<div class=\"loginbox\">Total Category Inputs by all of you</div><form>";
		my %categoryinfo;
		while (my $ref = $sth->fetchrow_hashref()) {
			$categoryinfo{$ref->{'category'}} = $categoryinfo{$ref->{'category'}}+$ref->{'count'};
		}
		print "<table>";
		foreach $key (sort(keys %categoryinfo)) {
			if ($categoryinfo{$key} == 0) {
				next;
			}
			my $string = "categoryview.cgi?showmycategory=$key";
			encode_entities($string);
	        print "<tr><td><a href =\"$string\"><text class=\"fontdec\">$key</text></a></td><td>
    			<input type=\"text\" value=\"$categoryinfo{$key}\" readonly></td></tr>";
	    }
	    print "</table>";
	    print "</form>
			   </div>
		</div>
	    </section>";
	    
	    $sth = $dbh->prepare("SELECT tag,tagcount FROM taginfo");
		$sth->execute();		
		print "<section class=\"registerdata\">
						<div class=\"loginbox\">Total Tag Inputs by all of you</div><form>";
		my %taginfo;
		while (my $ref = $sth->fetchrow_hashref()) {
			$taginfo{$ref->{'tag'}} = $taginfo{$ref->{'tag'}}+$ref->{'tagcount'};
		}
		print "<table>";
		foreach $key (sort(keys %taginfo)) {
			if ($taginfo{$key} == 0) {
				next;
			}
			my $string = "categoryview.cgi?showmycategory=$key";
			encode_entities($string);
	        print "<tr><td><a href =\"$string\"><text class=\"fontdec\">$key</text></a></td><td>
    			<input type=\"text\" value=\"$taginfo{$key}\" readonly></td></tr>";
	    }
	    print "</table>";
	    print "</form>
			   </div>
		</div>
	    </section>";
		
	print '</body>
	<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
	<hr width="65%">
	<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
</html>';


1;