#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use DBI;

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

if ($login == 1) {
	my $getuser = $session->param('logged_in_userid_mycp');
	my $url="profile.cgi?id=$getuser";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
} else {

	print '<html lang="en-US">
		<head>
			<title>My Copy-Pasta</title>
			<link rel="shortcut icon" href="images/newlogo.ico">
			<link rel="stylesheet" type="text/css" href="css/style.css">
			<link rel="stylesheet" type="text/css" href="css/viewstyle.css">
			<link rel="stylesheet" type="text/css" href="css/paragraph.css">
			<link rel="stylesheet" type="text/css" href="css/registerpasta.css">
			<div id="fb-root"></div>
			<script>(function(d, s, id) {
				  var js, fjs = d.getElementsByTagName(s)[0];
				  if (d.getElementById(id)) return;
				  js = d.createElement(s); js.id = id;
				  js.src = "//connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v2.4&appId=173510282674533";
				  fjs.parentNode.insertBefore(js, fjs);
				}(document, \'script\', \'facebook-jssdk\'));
			</script>
			<script>
				$(\'#repassword\').keyup(function(e){
			           if($(\'#regpwd\').val() !== $(\'#repassword\').val()){
			                $(\'#error\').removeClass(\'hidden\');
			                return false; 
			           }else{
			             $(\'#error\').addClass(\'hidden\');
			           }
			    });
			</script>
			<script>
			function myFunction() {
	    		var pass1 = document.getElementById("password").value;
			    var pass2 = document.getElementById("repassword").value;
			    var ok = true;
			    if (pass1 != pass2) {
			        //alert("Passwords Do not match");
			        document.getElementById("passwordmsg").innerHTML = \'Mismatch Password\';
			        document.getElementById("passwordmsg").style.backgroundColor  = "#E34234";
			        ok = false;
			    } else {
			    	//alert("Passwords match");
			        document.getElementById("passwordmsg").innerHTML = \'\';
			    }
			    return ok;
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
			</table>';
			
			print '<section class="registerdata">
				<div class="loginbox">Register yourself in Copy-Pasta</div>
				<form action="registerme.cgi" onsubmit="return myFunction()" METHOD="post" ENCTYPE="multipart/form-data">
					<text class="fontdec">Username</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="text" title="username" placeholder="username (no special characters only underscore allowed, 64 characters)" pattern="^([A-Za-z]|[0-9]|_)+$" style="width:70%" name="username" maxlength="64" required><br /><br />
					<text class="fontdec">Password</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="password" title="password" placeholder="minimum 6 characters" style="width:70%" name="password" id="password" maxlength="64" pattern=".{6,}" required><br /><br />
			    	<text class="fontdec">Retype Password</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="password" title="repassword" placeholder="retype your password (minimum 6 characters)" style="width:70%" name="repassword" id="repassword" maxlength="64" pattern=".{6,}"  required><br />
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<label id="passwordmsg"></label><br/>
			    	<text class="fontdec">Name</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="text" title="name" placeholder="your name" style="width:70%" name="name" id="name" maxlength="256" required><br /><br />
			    	<text class="fontdec">Email</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="text" title="email" placeholder="proper email address" style="width:70%" name="email" id="email" maxlength="512" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$" required><br /><br />
			    	<text class="fontdec">Display Picture</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<INPUT size=70 TYPE="file" name="file" accept=\".gif\"> (gif only, optional)<br /><br />
			    	<text class="fontdec">Date of birth</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="date" title="dob" style="width:70%" name="dob" id="dob" maxlength="128" required><br /><br />
			    	<text class="fontdec">Identity Lock</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="text" title="identitylock" placeholder="your identitylock (unique to your identity)" style="width:70%" name="identitylock" id="identitylock" maxlength="64" placeholder="maximum 64 characters, no special characters" required><br /><br />
					<text class="fontdec">Security Question</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="text" title="secquestion" style="width:70%" name="secquestion" id="secquestion" placeholder="your security (used in case of password misplace), 128 characters" maxlength="128" required><br /><br />
			    	<text class="fontdec">Security Answer</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="password" title="secanswer" style="width:70%" name="secanswer" id="secanswer" placeholder="your security answer for above question, 128 characters" maxlength="128" required><br /><br />
			    	<text class="fontdec">Occupation</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="text" title="occupation" style="width:70%" name="occupation" maxlength="128" placeholder="Profession like Student/Doctor/Engineer" required><br /><br />
			    	<text class="fontdec">Place</text>
			    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    		<input type="text" title="place" style="width:70%" name="place" maxlength="128" placeholder="Current Reciding City Or State" required><br /><br />
			    		
			    	<text class="fontdec">Account Type</text>
			    				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			    			<input type="text" style="width:70%" value="normal user account" readonly><br /><br />
			    			
			    	<input type="submit" class="submitbox" name="submit" alt="search" value="Register">
			    </form>
			</section>';
			
			
			print '</body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';
}

1;