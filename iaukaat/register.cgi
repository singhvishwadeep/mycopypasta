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
			<title>My iAukaat</title>
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
			
			<script type="text/javascript">
			function AlertFilesize(){
			    if(window.ActiveXObject){
			        var fso = new ActiveXObject("Scripting.FileSystemObject");
			        var filepath = document.getElementById(\'fileInput\').value;
			        var thefile = fso.getFile(filepath);
			        var sizeinbytes = thefile.size;
			    }else{
			        var sizeinbytes = document.getElementById(\'fileInput\').files[0].size;
			    }
			
			    var fSExt = new Array(\'Bytes\', \'KB\', \'MB\', \'GB\');
			    fSize = sizeinbytes; i=0;while(fSize>900){fSize/=1024;i++;}
			
			    alert((Math.round(fSize*100)/100)+\' \'+fSExt[i]);
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
			</table>';
			print '<section class="registerdata">
				<div class="loginbox">Register yourself in iAukaat</div>
				<text class="fontdec" style="padding:12px">Note:</text> <ul>
				  <li><b>username and password</b> must have minimum 6 characters.</li>
				  <li>only char, numbers, dot and underscore are allowed in <b>username</b>.</li>
				  <li>You should choose proper <b>email id</b>, for future references.</li>
				  <li><b>Identity Lock</b> can be any word or sentence which you think is unique to you like:
				  	<ul>
				      <li>Trust ME, I am an Engineer.</li>
				      <li>Yahooo!</li>
				    </ul>
				  </li>
				  <li><b>Identity Lock</b> is a string/identifier which will be used for identification in password recovery.</li>
				  <li><b>Security Question and Answer</b> is also necessary for password recovery.</li>
				  <li><b>Please</b> try to give proper information and donot misuse the application.</li>
				</ul>
				<br />
				<form action="registerme.cgi" onsubmit="return myFunction()" METHOD="post" ENCTYPE="multipart/form-data">
					<table>
					<tr><td><text class="fontdec">Username</text></td>
			    		<td><input type="text" title="username" placeholder="only underscore and dot allowed with chars/num (minimum 6)" pattern="^([A-Za-z]|[0-9]|_|\.){6,}$" style="width:100%" name="username" maxlength="64" required></td></tr>
					<tr><td><text class="fontdec">Password</text></td>
			    		<td><input type="password" title="password" placeholder="minimum 6 characters" style="width:100%" name="password" id="password" maxlength="64" pattern=".{6,}" required></td></tr>
			    	<tr><td><text class="fontdec">Retype Password</text></td>
			    		<td><input type="password" title="repassword" placeholder="retype your password (minimum 6 characters)" style="width:100%" name="repassword" id="repassword" maxlength="64" pattern=".{6,}"  required></td></tr>
			    	<tr><td></td><td><label id="passwordmsg"></label></td></tr>
			    	<tr><td><text class="fontdec">Name</text></td>
			    		<td><input type="text" title="name" placeholder="your name" style="width:100%" name="name" id="name" maxlength="256" required></td></tr>
			    	<tr><td><text class="fontdec">Email</text></td>
			    		<td><input type="text" title="email" placeholder="proper email address" style="width:100%" name="email" id="email" maxlength="512" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$" required></td></tr>
			    	<tr><td><text class="fontdec">Display Picture</text></td>
			    		<td><input size=70 id="fileInput" name="file" type="file" onchange="AlertFilesize();" accept=\".gif\" disabled/> <text style="color:red">(currently disabled)</text></td></tr>
			    	<tr><td><text class="fontdec">Date of birth</text></td>
			    		<td><input type="date" title="dob" style="width:100%" name="dob" id="dob" maxlength="128" required></td></tr>
			    	<tr><td><text class="fontdec">Identity Lock</text></td>
			    		<td><input type="text" title="identitylock" placeholder="your identitylock (unique to your identity)" style="width:100%" name="identitylock" id="identitylock" maxlength="64" placeholder="maximum 64 characters, no special characters" required></td></tr>
					<tr><td><text class="fontdec">Security Question</text></td>
			    		<td><input type="text" title="secquestion" style="width:100%" name="secquestion" id="secquestion" placeholder="your security (used in case of password misplace), 128 characters" maxlength="128" required></td></tr>
			    	<tr><td><text class="fontdec">Security Answer</text></td>
			    		<td><input type="password" title="secanswer" style="width:100%" name="secanswer" id="secanswer" placeholder="your security answer for above question, 128 characters" maxlength="128" required></td></tr>
			    	<tr><td><text class="fontdec">Occupation</text></td>
			    		<td><input type="text" title="occupation" style="width:100%" name="occupation" maxlength="128" placeholder="Profession like Student/Doctor/Engineer" required></td></tr>
			    	<tr><td><text class="fontdec">Place</text></td>
			    		<td><input type="text" title="place" style="width:100%" name="place" maxlength="128" placeholder="Current Reciding City Or State" required></td></tr>
			    	<tr><td><text class="fontdec">Account Type</text></td>
			    		<td><input type="text" style="width:100%" value="normal user account" readonly></td></tr>
			    	</table><br />
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