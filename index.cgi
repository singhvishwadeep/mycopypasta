#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
#use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session ('MYCOPYPASTASESSION');

my $err = 0;
my $session = CGI::Session->load();
my $var = $session->param('activelogin');
$q = new CGI;
print $q->header(-cache_control=>"no-cache, no-store, must-revalidate");


#print "GET ME -$session- ->$var<- ->$exp<- and ->$emp<-<br/>";
if($session->is_expired) {
	print "Session is_expired\n";
	#if session is expired then remove session and coookie
	require "www/cgi-bin/resetsession.cgi";
} elsif($session->is_empty) {
	print "Session is_empty\n";
	#if session is expired then remove session and coookie
	require "www/cgi-bin/resetsession.cgi";
} else {
	#print "Session is present --$var---\n";
	# if session is not expired
	if ($var eq "1") {
		# already logged in
		#print "already logged in\n";
		my $url="view.html";
		my $t=1; # time until redirect activates
		print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
	} else {
		#print "wrong password\n";
		# wrong password
		my $err = 1;
		$session->param('activelogin', "0");
	}
}

print '<html lang="en-US">
	<head>
		<title>My Copy-Pasta</title>
		<link rel="shortcut icon" href="images/newlogo.ico">
		<link rel="stylesheet" type="text/css" href="css/style.css">
		<link rel="stylesheet" type="text/css" href="css/viewstyle.css">
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
				        <li><a href="index.html">Home/Login/Profile</a></li>
				        <li><a href="#">About/Newsletter</a></li>
				        <li><a href="view.html">My Copies</a></li>
				        <li><a href="#">Tutorials</a></li>
				        <li><a href="#">Search</a></li>
				        <li><a href="#">Contact Us</a></li>
				      </ul>
				    </div>
				</td>
			</tr>
		</table>
		<section class="login">
			<div class="loginbox">My Copy Pasta Login</div>
			<form action="www/cgi-bin/validate.cgi" method="post" autocomplete="off">
		    	<input type="text" required title="Username required" placeholder="Username" name="User" autocomplete="off">
		        <input type="password" required title="Password required" placeholder="Password" name="Password"><br /><br />
		        <input type="submit" class="submitbox" name="submit" alt="search" value="Submit">
		        <div class="otherbox">
		        	<div class="colorme"><a href="register.html">Register</a></div>
		            <div class="colorme"><a href="#">Forgot Password?</a></div>
		        </div>
		    </form>
		</section>
	</body>
	<div style="text-align:center"><text style="color:grey;font-size:12px">©2015 Vishwadeep Singh My Copy-Pasta</text></div>
	<hr width="65%">
	<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
</html>';


1;