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
	my $url="login.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
} else {
	# cookie has some value, hence loading session from $ssid
	$session = CGI::Session->load($ssid) or die "$!";
	if($session->is_expired || $session->is_empty) {
		# if session is expired/empty, need to relogin
		my $url="login.cgi";
		my $t=0; # time until redirect activates
		print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
	} else {
		my $value = $session->param('logged_in_status_mycp');
		if ($value eq "1") {
			# properly logged in
			$login = 1;
		} else {
			my $url="login.cgi";
			my $t=0; # time until redirect activates
			print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
		}
	}
}

my $trrid = $q->param('id');

if ($login) {
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
			my $getuser = $session->param('logged_in_userid_mycp');
			my $sth = $dbh->prepare("SELECT tid,date,time,userid,amount,account,type,category,tags,ip,http_agent,comment FROM transactioninfo where userid='$getuser' and tid='$trrid'");
			$sth->execute();
			my $tid = -1;
			my $date;
			my $time;
			my $userid;
			my $amount;
			my $account;
			my $type;
			my $category;
			my $tags;
			my $ip;
			my $http_agent;
			my $comment;
			while (my $ref = $sth->fetchrow_hashref()) {
				$tid = $ref->{'tid'};
				$date = $ref->{'date'};
				$time = $ref->{'time'};
				$userid = $ref->{'userid'};
				$amount = $ref->{'amount'};
				$account = $ref->{'account'};
				$type = $ref->{'type'};
				$category = $ref->{'category'};
				$tags = $ref->{'tags'};
				$ip = $ref->{'ip'};
				$http_agent = $ref->{'http_agent'};
				$comment = $ref->{'comment'};
				break;
			}
			if ($tid == -1) {
				print '<tr><td><text style="color:red;font-size:24px;">Transaction ID not found.</text></td></tr></table>';
			} else {
				print '<tr><td><section class="registerdata">
					<div class="loginbox">transaction';
					print " $tid";
					print ' in iAukaat <a class="edit_button" href="edittransaction.cgi?id=';
					print $tid;
					print '"><img src="images/edit.jpg" alt="Edit" style="width:10px;height:10px;padding-right:3px">Edit</a></div>
						<form> 		<table>
						<tr><td><text class="fontdec">Amount</text></td>
				    		<td><input type="text" maxlength="64" ';
				    	print "value=\"$amount\"";
				    	print ' readonly></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">Account</text></td>
				    		<td><input type="text" maxlength="64" ';
				    	print "value=\"$account\"";
				    	print ' readonly></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">Transaction Type</text></td>
				    		<td><input type="text" maxlength="64" ';
				    	print "value=\"$type\"";
				    	print ' readonly></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">Date</text></td>
				    		<td><input type="text" maxlength="64" ';
				    	print "value=\"$date\"";
				    	print ' readonly></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">Time</text></td>
				    		<td><input type="text" maxlength="64" ';
				    	print "value=\"$time\"";
				    	print ' readonly></td></tr>';	
				    	
				    	print '<tr><td><text class="fontdec">Category</text></td>
				    		<td><input type="text" maxlength="128" ';
				    	print "value=\"$category\"";
				    	print ' readonly></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">Tags</text></td>
				    		<td><input type="text" maxlength="128" ';
				    	print "value=\"$tags\"";
				    	print ' readonly></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">IP Address</text></td>
				    		<td><input type="text" maxlength="64" ';
				    	print "value=\"$ip\"";
				    	print ' readonly></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">Comment</text></td>
				    		<td><input type="text" maxlength="512" ';
				    	print "value=\"$comment\"";
				    	print ' readonly></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">HTTP Agent</text></td>
				    		<td><input type="text" maxlength="512" ';
				    	print "value=\"$http_agent\"";
				    	print ' readonly></td></tr>';
				    	
						print '</table><br />
				    </form>
				</section>';
				print '</table>';
			}
		print '</body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';
}

1;