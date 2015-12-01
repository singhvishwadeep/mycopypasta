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

my $profileid = $q->param('id');

if ($login == 0 || $profileid eq "") {
	my $url="index.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
} elsif ($login == 1 && $session->param('logged_in_userid_mycp') ne $profileid) {
	my $url="index.cgi";
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
					        print '<li><a href="addaccount.cgi">Add New Account</a></li>';
					        print '<li><a href="logout.cgi">Logout</a></li>';
					        print "<li><a href=\"profile.cgi?id=$getuser\">My Profile</a></li>";
				        } else {
				        	print '<li><a href="login.cgi">Login</a></li>';
				        }
				      print '<li><a href="contact.cgi">Contact iAukaat Team</a></li></ul>
				    </div>
					</td>
				</tr>';
			
			my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
			my $dbh = DBI->connect($dsn,"root","");
			my $sth = $dbh->prepare("SELECT myusername,mydob,name,displaypic,registereddate,myemail,myprofession,myplace,activeaccount,admin,myidentitylock,mysecurityquestion,mysecurityanswer FROM userdatabase where id='$profileid' and deleted=0");
			$sth->execute();
			my $countres = $sth->rows;
			if ($countres == 0) {
				print "<tr><td><font color=\"red\">No Pofile Found.</font></td></tr></table>";
			} else {
				my $name = "";
				my $username = "";
				my $displaypic = "";
				my $registereddate = "";
				my $email = "";
				my $occupation = "";
				my $place = "";
				my $activeaccount = "";
				my $admin = "";
				my $dob = "";
				my $identitylock = "";
				my $secquestion = "";
				my $secanswer = "";
				
				while (my $ref = $sth->fetchrow_hashref()) {
					$username = $ref->{'myusername'};
					$name = $ref->{'name'};
					$displaypic = $ref->{'displaypic'};
					$registereddate = $ref->{'registereddate'};
					$email = $ref->{'myemail'};
					$occupation = $ref->{'myprofession'};
					$place = $ref->{'myplace'};
					$activeaccount = $ref->{'activeaccount'};
					$admin = $ref->{'admin'};
					$dob = $ref->{'mydob'};
					$identitylock = $ref->{'myidentitylock'};
					$secquestion = $ref->{'mysecurityquestion'};
					$secanswer = $ref->{'mysecurityanswer'};
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
			
				print "</table><section class=\"registerdata\">
					<div class=\"loginbox\">Edit your Profile</div>
					<form action=\"editme.cgi\" METHOD=\"post\" ENCTYPE=\"multipart/form-data\">
					<table>
						<tr><td><text class=\"fontdec\">Username</text></td>
				    		<td><input type=\"text\" style=\"width:70%;background:grey\" name=\"username\" value=\"$username\" readonly></td></tr>
				    	<tr><td><text class=\"fontdec\">Profile ID</text></td>
				    		<td><input type=\"text\" style=\"width:70%;background:grey\" name=\"id\" value=\"$profileid\" readonly></td></tr>
				    	<tr><td><text class=\"fontdec\">Name</text></td>
				    		<td><input type=\"text\" title=\"name\" placeholder=\"your name\" value=\"$name\" style=\"width:70%\" name=\"name\" id=\"name\" maxlength=\"256\" required></td></tr>
				    	<tr><td><text class=\"fontdec\">Email</text></td>
				    		<td><input type=\"text\" title=\"email\" placeholder=\"proper email address\" style=\"width:70%;background:grey\" name=\"email\" id=\"email\" maxlength=\"512\" value=\"$email\" ";
				    		print 'pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$" ';
				    		print "readonly></td></tr>
				    	<tr><td><text class=\"fontdec\">Display Picture</text></td>
				    		<td><input size=70 id=\"fileInput\" name=\"file\" type=\"file\" onchange=\"AlertFilesize();\" accept=\".gif\" disabled/> <text style=\"color:red\">(currently disabled)</text></td></tr>
				    	<tr><td><text class=\"fontdec\">Date of birth</text></td>
				    		<td><input type=\"text\" title=\"dob\" style=\"width:70%\" name=\"dob\" id=\"dob\" value=\"$dob\" maxlength=\"128\" required></td></tr>
				    	<tr><td><text class=\"fontdec\">Identity Lock</text></td>
				    		<td><input type=\"text\" title=\"identitylock\" placeholder=\"your identitylock (unique to your identity)\" value=\"$identitylock\" style=\"width:70%\" name=\"identitylock\" id=\"identitylock\" maxlength=\"64\" placeholder=\"any private key (64c) another than password, no special chars\" required></td></tr>
						<tr><td><text class=\"fontdec\">Security Question</text></td>
				    		<td><input type=\"text\" title=\"secquestion\" style=\"width:70%\" name=\"secquestion\" id=\"secquestion\" placeholder=\"your security (used in case of password misplace), 128 characters\" maxlength=\"128\" value=\"$secquestion\"  required></td></tr>
				    	<tr><td><text class=\"fontdec\">Security Answer</text></td>
				    		<td><input type=\"text\" title=\"secanswer\" style=\"width:70%\" name=\"secanswer\" id=\"secanswer\" placeholder=\"your security answer for above question, 128 characters\" maxlength=\"128\" value=\"$secanswer\" required></td></tr>
				    	<tr><td><text class=\"fontdec\">Occupation</text></td>
				    		<td><input type=\"text\" title=\"occupation\" style=\"width:70%\" name=\"occupation\" maxlength=\"128\" placeholder=\"Profession like Student/Doctor/Engineer\" value=\"$occupation\" required></td></tr>
				    	<tr><td><text class=\"fontdec\">Place</text></td>
				    		<td><input type=\"text\" title=\"place\" style=\"width:70%\" name=\"place\" maxlength=\"128\" placeholder=\"Current Reciding City Or State\" value=\"$place\"  required></td></tr>
				    	<tr><td><text class=\"fontdec\">Account Type</text></td>
				    		<td><input type=\"text\" style=\"width:70%;background:grey\" value=\"$account\" readonly></td></tr>
				   </table><br/>
				    	<input type=\"submit\" class=\"submitbox\" name=\"submit\" alt=\"search\" value=\"Submit Changes\">
				    	OR</text><br /> <a href=\"deleteprofilebyid.cgi?id=$profileid\" class=\"button_delete\" onclick=\"return confirm('Are you sure you want to delete your account?');\">Delete Your account</a><br /><br />
				    </form>
				</section>";
			
			}
			
			print '</body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';
}

1;