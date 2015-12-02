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
				
				print "<tr><td><font style=\"font-family: Georgia;font-size: 16px;font-weight: bold;color: #600;\">Current Accounts</font></td></tr>";
				
				print '<tr><td><table align="center" width="100%">';
				
				my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
				my $dbh = DBI->connect($dsn,"root","");
				my $getuser = $session->param('logged_in_userid_mycp');
				my $sth = $dbh->prepare("select account,type,balance from traccountinfo where userid='$getuser'");
				$sth->execute();
				my %allaccounts;
				my %allaccountstype;
				while (my $ref = $sth->fetchrow_hashref()) {
					$allaccounts{$ref->{'account'}} = 0;
					$allaccountstype{$ref->{'account'}} = $ref->{'type'};
				}
				my $getuser = $session->param('logged_in_userid_mycp');
				$sth = $dbh->prepare("select amount,account,type from transactioninfo where userid='$getuser'");
				$sth->execute();
				while (my $ref = $sth->fetchrow_hashref()) {
					if ($ref->{'type'} eq "Expence") {
						$allaccounts{$ref->{'account'}} = $allaccounts{$ref->{'account'}} - $ref->{'amount'};
					} else {
						$allaccounts{$ref->{'account'}} = $allaccounts{$ref->{'account'}} + $ref->{'amount'};
					}
				}
				
				print "<tr style=\"background-color: #D94E67;color: white;\"><th>S.No.</th><th>Account</th><th>Type</th><th>Balance</th></tr>";
				my $i = 1;
				my $tot = 0;
			foreach my $acc (keys %allaccounts) {
				my $line = "";
				if ($i%2 == 0) {
					$line = "background-color: #ff5050;color: white;";
				} else {
					$line = "background-color: #999966;color: white;";
				}
				$tot = $tot + $allaccounts{$acc};
				print "<tr align=\"center\" style=\"$line\"><td>$i</td><td><a href=\"byaccount.cgi?id=$acc\" target=\"_blank\">$acc</a></td><td>$allaccountstype{$acc}</td><td>$allaccounts{$acc}</td></tr>";
				$i++;
			}
				print "<tr align=\"center\" style=\"background-color: #000000;color: white;\"><td></td><td></td><td>Total</td><td>$tot</td></tr>";
				print '</table></td></tr>';
				
				print '<tr><td><section class="registerdata">
						<div class="loginbox">Add new Account in iAukaat</div>
						<form action="addaccountnew.cgi" METHOD="post" ENCTYPE="multipart/form-data">
							<table>
							<tr><td><text class="fontdec">Account</text></td>
					    		<td><input type="text" title="account" placeholder="account name" style="width:100%" name="account" id="account" maxlength="64" required></td></tr>
							<tr><td><text class="fontdec">Account Type</text></td>
					    		<td><select id="ttype" name="ttype"><option selected value="credit">credit</option><option value="debit">debit</option></select></td></tr>
							<tr><td><text class="fontdec">Balance</text></td>
					    		<td><input type="text" title="balance" placeholder="initial balance (optional)" style="width:100%" name="balance" id="balance" maxlength="64" pattern="^[0-9]\d*(\.\d+)?$"></td></tr>
					    	</table><br />
					    	<input type="submit" class="submitbox" name="submit" alt="search" value="Submit">
					    </form>
					</section></td></tr>';
				
				
			print '</table>
		</body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';
}

1;