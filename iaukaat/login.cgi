#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use Digest::MD5 qw(md5 md5_hex md5_base64);

# new cgi query
my $q = new CGI;
# fetching cookie
my $ssid = $q->cookie('MYCOPYPASTACOOKIE');
# printing header
print $q->header;
# login error or not
my $err = 0;
my $msg = $q->param('error');
# proper logged in?
my $login = 0;

if ($msg ne "") {
	if (md5_hex('0') eq $msg) {
		$msg = 0;
		$err = 1;
	} elsif (md5_hex('1') eq $msg) {
		$msg = 1;
		$err = 1;
	} elsif (md5_hex('2') eq $msg) {
		$msg = 2;
		$err = 1;
	}
}

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
			my $url="index.cgi";
			my $t=0; # time until redirect activates
			print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
		} else {
			#wrong password/ some error
			$err = 1;
		}
	}
}

if ($login == 0) {
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
					        print '<li><a href="addtransaction.cgi">Add Transaction</a></li>';
				        }
				        print '<li><a href="view.cgi">iAukaat</a></li>
				        <li><a href="tutorial.cgi">Tutorials</a></li>
				        <li><a href="search.cgi">Search Transaction</a></li>
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
				</tr>
			</table>
			<section class="login">
				<div class="loginbox">My Copy-Pasta Login</div>
				<form action="validate.cgi" method="post" autocomplete="off">
			    	<input type="text" required title="Username required" placeholder="Username" name="User" autocomplete="off">
			        <input type="password" required title="Password required" placeholder="Password" name="Password"><br /><br />
			        <input type="submit" class="submitbox" name="submit" alt="search" value="Submit">';
	if ($err) {
			#msg = 0; account deleted
			#msg = 1; account is not activated
			#msg = 2; wrong username/password
			if ($msg == 0) {
				print "<div class=\"colorerr\">Account is deleted</div>";
			} elsif ($msg == 1) {
				print "<div class=\"colorerr\">Account is not activated</div>";
			} else {
				print "<div class=\"colorerr\">Wrong username/password</div>";
			}
	}
			        
					print '<div class="otherbox">
							<div class="colorme"><a href="register.cgi">Register</a></div>
			            <div class="colorme"><a href="forgotpwd.cgi">Forgot Password?</a></div>
			        </div>
			    </form>
			</section>
		</body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';

}
1;