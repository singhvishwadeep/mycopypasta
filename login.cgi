#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;

my $q = new CGI;
my $value = $q->cookie('MYCOPYPASTACOOKIE');
print $q->header;
my $err = 0;
my $login = 0;
if($value eq "") {
	#print "Cookie is empty/not set\n";
	#Empty cookie found, remove if cookie found
	#require "removecookie.cgi";
#	my $cookie1 = CGI::Cookie->new(-name=>'MYCOPYPASTACOOKIE',-value=>'',-expires=>'now');
} else {
	#if session is not expired
	if ($value eq "1") {
		#already logged in
		#print "already logged in\n";
#		my $url="view.html";
#		my $t=1;
#		print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
		$login = 1;
	} else {
		#print "wrong username/password\n";
		#wrong password
		$err = 1;
		#require "removecookie.cgi";
#		my $cookie1 = CGI::Cookie->new(-name=>'MYCOPYPASTACOOKIE',-value=>'',-expires=>'now');
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
			</tr>
		</table>
		<section class="login">
			<div class="loginbox">My Copy-Pasta Login</div>
			<form action="validate.cgi" method="post" autocomplete="off">
		    	<input type="text" required title="Username required" placeholder="Username" name="User" autocomplete="off">
		        <input type="password" required title="Password required" placeholder="Password" name="Password"><br /><br />
		        <input type="submit" class="submitbox" name="submit" alt="search" value="Submit">';
if ($err) {
	print '<div class="colorerr">Wrong username/Password</div>';
}
		        
				print '<div class="otherbox">
						<div class="colorme"><a href="register.cgi">Register</a></div>
		            <div class="colorme"><a href="forgotpwd.cgi">Forgot Password?</a></div>
		        </div>
		    </form>
		</section>
	</body>
	<div style="text-align:center"><text style="color:grey;font-size:12px">©2015 Vishwadeep Singh My Copy-Pasta</text></div>
	<hr width="65%">
	<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
</html>';


1;