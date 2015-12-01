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

if ($login == 0) {
	my $url="index.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
} elsif ($login == 1 && $session->param('logged_in_user_mycp') ne "admin") {
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
				var checkflag = "false";
				function check(field) {
				  if (checkflag == "false") {
				    for (i = 0; i < field.length; i++) {
				      field[i].checked = true;
				    }
				    checkflag = "true";
				    return "Uncheck All";
				  } else {
				    for (i = 0; i < field.length; i++) {
				      field[i].checked = false;
				    }
				    checkflag = "false";
				    return "Check All";
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
				
				my $query = "select id,myusername,name from userdatabase where activeaccount=0 AND deleted=0";
				my $sth = $dbh->prepare($query);
				$sth->execute();
				print "<tr><td><form name=myform action=\"performactivation.cgi\" method=post><input type=button value=\"Check All\" onClick=\"this.value=check(this.form.list)\"><br />";
				while (my $ref = $sth->fetchrow_hashref()) {
					my $userid = $ref->{'id'};
					my $username = $ref->{'myusername'};
					my $name = $ref->{'name'};
					print "<input type=checkbox name=list value=\"$userid\"><a href=\"profile.cgi?id=$userid\" target=\"_blank\">$name $userid</a><br />";
				}
				
			print '<input type="submit" name="submit" alt="search" value="Activate Accounts"></form></td></tr></table></body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';
}

1;