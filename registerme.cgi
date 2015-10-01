#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use DBI;
use DBD::mysql;
use POSIX 'strftime';

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
	my $url="index.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
}


sub  trim { 
	my $s = shift;
	$s =~ s/^\s+|\s+$//g;
	return $s;
}

my $username=param('username');
my $name=param('name');
my $password=param('password');
my $email=param('email');
my $filename=param('file');
my $dob=param('dob');
my $identitylock=param('identitylock');
my $secquestion=param('secquestion');
my $secanswer=param('secanswer');
my $occupation=param('occupation');
my $place=param('place');

$username = trim($username);
$name = trim($name);
$password = trim($password);
$email = trim($email);
$filename = trim($filename);
$dob = trim($dob);
$identitylock = trim($identitylock);
$secquestion = trim($secquestion);
$secanswer = trim($secanswer);
$occupation = trim($occupation);
$place = trim($place);

my $usernameexists = 0;
my $emailexists = 0;
	
if ($username ne "" && $password ne "" && $email ne "") {

	
	my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
	my $dbh = DBI->connect($dsn,"root","");
	my $sth = $dbh->prepare("SELECT id FROM userdatabase where myusername='$username'");
	$sth->execute();
	while (my $ref = $sth->fetchrow_hashref()) {
		$usernameexists = 1;
	}
	
	$sth = $dbh->prepare("SELECT id FROM userdatabase where myemail='$email'");
	$sth->execute();
	while (my $ref = $sth->fetchrow_hashref()) {
		$emailexists = 1;
	}
	
	$sth->finish();
	
	my $errmessage = "";
	
	if ($emailexists == 1 || $usernameexists == 1) {
		$dbh->disconnect();
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
		
		if ($emailexists == 1 || $usernameexists == 1) {
			if ($emailexists == 1) {
				print '<tr><td><ul><li><font size="3" color="red">Email already Registered</font></li></ul></td></tr>';
			}
			if ($usernameexists == 1) {
				print '<tr><td><ul><li><font size="3" color="red">Username already exists</font></li></ul></td></tr>';
			}
			print '<tr><td>
			<FORM>
			<INPUT TYPE="button" VALUE="Go Back to Redit the Values" onClick="history.go(-1)" style="width:250px;margin-left: 35px;display: block;background:red">
			</FORM>
			</td></tr>';
		} elsif ($username ne "" && $password ne "" && $email ne "") {
			# register the user
			my $ip = $ENV{REMOTE_ADDR};
			my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
			my $dbh = DBI->connect($dsn,"root","");
			$sth = $dbh->prepare("INSERT into userdatabase ( myusername,mydob,name,mypassword,registeredip,registereddate,myemail,myidentitylock,mysecurityquestion,mysecurityanswer,myprofession,myplace ) VALUES ( '$username','$dob', '$name','$password', '$ip',NOW(),'$email','$identitylock','$secquestion','$secanswer','$occupation','$place')");
			$sth->execute();
			$sth->finish();
			
			if ($filename ne "") {
				my $userid = -1;
			
				$sth = $dbh->prepare("SELECT id FROM userdatabase where myusername='$username'");
				$sth->execute();
				while (my $ref = $sth->fetchrow_hashref()) {
					$userid = $ref->{'id'};
				}
				$sth->finish;
				my $Date = strftime '%Y-%m-%d', localtime;
				my $upload_dir = "images/$Date\_uploaded_files";
				mkdir "$upload_dir", 0777 unless -d "$upload_dir";
				$filename =~ s/.*[\/\\](.*)/$1/;
				$filename =~ s/ /_/g;
				my $upload_filehandle = $q->upload("file");
				my $directory_filename = "$upload_dir/$filename";
				# upload the file to the server
				open UPLOADFILE, ">$directory_filename";
				binmode UPLOADFILE;
				while ( <$upload_filehandle> )
				{
				    print UPLOADFILE;
				}
				close UPLOADFILE;
				# Open the file
				open MYFILE, $directory_filename || print "Cannot open file";
				my $blob_file;
				# Read in the contents
				while (<MYFILE>) {
				    $blob_file .= $_;
				}
				close MYFILE;
				$query = "update userdatabase set displaypic=? where id=?";
				$sth = $dbh->prepare($query);
				$sth->execute($blob_file,$userid) || print "Can't access database";
				$sth->finish;
				$dbh->disconnect();
				unlink $directory_filename;
			}

			print "<tr><td><font color=\"green\">Congratulations. $username got registered with us. Wait for admin to activate your account. Try <a href=\"login.cgi\">Login Here</a></font></td></tr>";
		} else {
				my $url="index.cgi";
				my $t=0; # time until redirect activates
				print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
		}
		
		print '</table>
	</body>
	<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">©2015 My Blue Sky Labs, powered by Vishwadeep Singh</text></div>
	<hr width="65%">
	<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
</html>';


1;