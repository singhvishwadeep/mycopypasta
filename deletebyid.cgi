#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use DBI;
use HTML::Entities;
use Scalar::Util qw(looks_like_number);

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

sub  trim { 
	my $s = shift;
	$s =~ s/^\s+|\s+$//g;
	return $s;
}

if ($login == 0) {
	my $url="login.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
} else {

	my $editid = $q->param('id');
	
	if (looks_like_number($editid)) {
	  
	} else {
		$editid = 0;
	}
	
	my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
	my $dbh = DBI->connect($dsn,"root","");
	my $getuser = $session->param('logged_in_userid_mycp');
	my $getusername = $session->param('logged_in_user_mycp');
	
	my $edituserid = -1;
	my $query = "select user from datasubmission where id='$editid' AND showme=1";
	my $sth = $dbh->prepare($query);
	$sth->execute();
	while (my $ref = $sth->fetchrow_hashref()) {
		$edituserid = $ref->{'user'};
		break;
	}
	if ($edituserid == $getuser) {
		print '<html lang="en-US">
			<head>
				<title>My Copy-Pasta</title>
				<link rel="shortcut icon" href="images/newlogo.ico">
				<link rel="stylesheet" type="text/css" href="css/style.css">
				<link rel="stylesheet" type="text/css" href="css/viewstyle.css">
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
				<script type="text/javascript">
				function changetextbox()
				{
				    document.getElementById("new_category").disabled=\'\';
					if (document.getElementById("selectcategory").value != "Create New Category") {
					    document.getElementById("new_category").disabled=\'true\';
					} else {
					    document.getElementById("new_category").disabled=\'\';
					}
				}
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
							        print '<li><a href="logout.cgi">Logout</a></li>
							        <li><a href="profile.cgi">Profile</a></li>';
						        } else {
						        	print '<li><a href="login.cgi">Login</a></li>';
						        }
						      print '</ul>
						    </div>
						</td>
					</tr>';
				
				$query = "update datasubmission set showme=0 where id = '$editid'";
				$sth = $dbh->prepare($query);
				$sth->execute();
				print "<tr><td><font color=\"red\">Copy-Pasta ID: $editid is deleted. If needed back, please contact admin <a href=\"mailto:myblueskylabs@gmail.com ?Subject=Reg:Retreive%20Copy-Pasta\" target=\"_top\">(Send Mail to myblueskylabs@gmail.com)</a> for retrieving it back.</font></td></tr>";
				print '</table></body>
			<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
			<hr width="65%">
			<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
		</html>';
	} else {
print '<html lang="en-US">
			<head>
				<title>My Copy-Pasta</title>
				<link rel="shortcut icon" href="images/newlogo.ico">
				<link rel="stylesheet" type="text/css" href="css/style.css">
				<link rel="stylesheet" type="text/css" href="css/viewstyle.css">
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
				<script type="text/javascript">
				function changetextbox()
				{
				    document.getElementById("new_category").disabled=\'\';
					if (document.getElementById("selectcategory").value != "Create New Category") {
					    document.getElementById("new_category").disabled=\'true\';
					} else {
					    document.getElementById("new_category").disabled=\'\';
					}
				}
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
							        print '<li><a href="logout.cgi">Logout</a></li>
							        <li><a href="profile.cgi">Profile</a></li>';
						        } else {
						        	print '<li><a href="login.cgi">Login</a></li>';
						        }
						      print '</ul>
						    </div>
						</td>
					</tr>';
				
				print "<tr><td><font color=\"red\">For Copy-Pasta ID: $editid, permission denied. If something wrong, please contact admin <a href=\"mailto:myblueskylabs@gmail.com ?Subject=Reg:Permission%20issue\" target=\"_top\">(Send Mail to myblueskylabs@gmail.com)</a> for the issue.</font></td></tr>";
				print '</table></body>
			<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
			<hr width="65%">
			<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
		</html>';
	}

}
1;