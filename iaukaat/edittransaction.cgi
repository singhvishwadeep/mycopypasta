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
				print '</table><section class="registerdata">
					<div class="loginbox">transaction for iAukaat</div>
						<form action="edittransactionsave.cgi" onsubmit="return myFunction()" METHOD="post" ENCTYPE="multipart/form-data">
						<table>';
						
						print '<tr><td><text class="fontdec">Transaction ID</text></td>
				    		<td><input type="text" maxlength="512"  title="tid" style="width:100%" name="tid" id="tid" ';
				    	print "value=\"$tid\"";
				    	print ' readonly></td></tr>';
				    	
				    	
						print '<tr><td><text class="fontdec">Amount</text></td>
				    		<td><input type="text" title="amount" style="width:100%" name="amount" maxlength="64" pattern="^[0-9]\d*(\.\d+)?$" ';
				    	print "value=\"$amount\"";
				    	print ' required></td></tr>';
				    	print '<tr><td><text class="fontdec">Account</text></td>';
				    	
				    	print '<td><select id="selectaccount" name="selectaccount">';
						$sth = $dbh->prepare("SELECT distinct(account) FROM traccountinfo where userid='$userid'");
						$sth->execute();
						while (my $ref = $sth->fetchrow_hashref()) {
							if ($ref->{'account'} ne "") {
								my $opt = "";
								if ($ref->{'account'} eq $account) {
									$opt = "selected";
								}
								print " <option $opt value=\"$ref->{'account'}\">$ref->{'account'}</option>";
							}
						}
						print '</select></td></tr>';
						
						print '<tr><td><text class="fontdec">Transaction Type</text></td>';
				    	
				    	print '<td><select id="ttype" name="ttype">';
						if ($type eq "Expence") {
							print " <option selected value=\"Expence\">Expence</option>";
							print " <option value=\"Income\">Income</option>";
						} else {
							print " <option value=\"Expence\">Expence</option>";
							print " <option selected value=\"Income\">Income</option>";
						}
						print '</select></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">Category</text></td>
							<td><select id="selectcategory" name="selectcategory" onChange="changetextbox();"><option value="Create New Category">Create New Category</option>';
					
						$sth = $dbh->prepare("SELECT distinct(category) FROM trcategoryinfo where userid='$getuser'");
						$sth->execute();
						while (my $ref = $sth->fetchrow_hashref()) {
							if ($ref->{'category'} ne "") {
								my $opt = "";
								if ($ref->{'category'} eq $category) {
									$opt = "selected";
								}
								print " <option $opt value=\"$ref->{'category'}\">$ref->{'category'}</option>";
							}
						}
						print '</select><input required type="text" title="new_category" placeholder="New Category (max 128 characters)" id="new_category" name="new_category" maxlength="128" disabled/></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">Tags</text></td>
				    		<td><input type="text" maxlength="512"  title="tags" style="width:100%" name="tags" id="tags" ';
				    	print "value=\"$tags\"";
				    	print ' required></td></tr>';
				    	
				    	print '<tr><td><text class="fontdec">Comment</text></td>
				    		<td><input type="text" maxlength="512"  title="comment" style="width:100%" name="comment" id="comment" ';
				    	print "value=\"$comment\"";
				    	print ' required></td></tr>';
				    	
						print '</table><br />
				    	<input type="submit" class="submitbox" name="submit" alt="search" value="Submit">
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