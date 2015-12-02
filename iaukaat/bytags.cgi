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

my $tagss = $q->param('id');
if ($login && $tagss ne "") {
	print '<html lang="en-US">
		<head>
			<title>My iAukaat</title>
			<link rel="shortcut icon" href="images/newlogo.ico">
			<link rel="stylesheet" type="text/css" href="css/style.css">
			<link rel="stylesheet" type="text/css" href="css/viewstyle.css">
			<link rel="stylesheet" type="text/css" href="css/paragraph.css">
			<div id="fb-root"></div>
			<script>(function(d, s, id) {
				  var js, fjs = d.getElementsByTagName(s)[0];
				  if (d.getElementById(id)) return;
				  js = d.createElement(s); js.id = id;
				  js.src = "//connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v2.4&appId=173510282674533";
				  fjs.parentNode.insertBefore(js, fjs);
				}(document, \'script\', \'facebook-jssdk\'));
			</script>';
				
			
		my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
		my $dbh = DBI->connect($dsn,"root","");
		my $getuser = $session->param('logged_in_userid_mycp');
		my $sth = $dbh->prepare("select distinct(account),type from traccountinfo where userid='$getuser'");
		$sth->execute();
		my %allaccounts;
		while (my $ref = $sth->fetchrow_hashref()) {
			if ($ref->{'type'} eq "credit") {
				$allaccounts{$ref->{'account'}} = -1;
			} else {
				$allaccounts{$ref->{'account'}} = 0;
			}
		}
		
		$sth = $dbh->prepare("select amount, account,new_value,date, prev_value,type,tags from transactioninfo where userid='$getuser' ORDER BY tid ASC");
		$sth->execute();
		my %dataexp;
		my %datainc;
		my %alldata;
		my %refarr;
		my @listarrdate;
		while (my $ref = $sth->fetchrow_hashref()) {
			my @values = split(',', $ref->{'tags'});
			my $pres = 0;
			foreach my $val (@values) {
				if ($val eq $tagss) {
					$pres = 1;
					break;
				}
			}
			if ($pres == 0) {
				next;
			}
			if ($ref->{'type'} eq "Expence") {
				if( exists($dataexp{$ref->{'date'}}) ){
					$dataexp{$ref->{'date'}} =  $dataexp{$ref->{'date'}} + $ref->{'amount'};
				} else{
					$dataexp{$ref->{'date'}} = $ref->{'amount'};
				}
				if( exists($alldata{$ref{'date'},$ref{'account'}}) ) {
					$alldata{$ref{'date'},$ref{'account'}} = $alldata{$ref{'date'},$ref{'account'}} - $ref->{'amount'};
				} else {
					$alldata{$ref{'date'},$ref{'account'}} = 0 - $ref->{'amount'};
				}
			} elsif ($ref->{'type'} eq "Income") {
				if( exists($datainc{$ref->{'date'}}) ){
					$datainc{$ref->{'date'}} =  $datainc{$ref->{'date'}} + $ref->{'amount'};
				} else{
					$datainc{$ref->{'date'}} = $ref->{'amount'};
				}
				if( exists($alldata{$ref{'date'},$ref{'account'}}) ) {
					$alldata{$ref{'date'},$ref{'account'}} = $alldata{$ref{'date'},$ref{'account'}} + $ref->{'amount'};
				} else {
					$alldata{$ref{'date'},$ref{'account'}} = $ref->{'amount'};
				}
			}
			if( !exists($refarr{$ref->{'date'}}) ){
				$refarr{$ref->{'date'}} = 1;
				push(@listarrdate, $ref->{'date'});
			}
		}
		
		print "<script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>\n";
		print "<script type=\"text/javascript\">\n";
		print "google.load('visualization', '1.1', {packages: ['line']});\n";
		print "google.setOnLoadCallback(drawChart);\n";
		print "function drawChart() {\n";

		print "var data = new google.visualization.DataTable();\n";
		print "data.addColumn('number', 'Days');\n";
		print "data.addColumn('number', 'Expence');\n";
		print "data.addColumn('number', 'Income');\n";
		print "data.addColumn('number', 'Total');\n";

		print "data.addRows([\n";
		my $i = 0;
		my $allshow = 0;
		my $finall = 0.0;
		foreach my $i1 (0 .. $#listarrdate) {
			my $ddate = $listarrdate[$i1];
			my $exp = 0.0;
			if( exists($dataexp{$ddate}) ){
				$exp = $dataexp{$ddate};
			}
			my $inc = 0.0;
			if( exists($datainc{$ddate}) ){
				$inc = $datainc{$ddate};
			}
			my $tot = $allshow+$inc-$exp;
			$allshow = $tot;
			$tot = 0;
			print "[$i,$exp,$inc,$tot],\n";
			$finall = $tot;
			$i++;
		}
		print "]);\n";
		my $getusern = $session->param('logged_in_user_mycp');
		print "var options = {\n";
		print "chart: {\n";
        print "  title: 'iAukaat Balance for $getusern',\n";
        print "  subtitle: 'in Indian Rupees'\n";
        print " },\n";
		print "height: 500\n";
		print "};\n";

		print "var chart = new google.charts.Line(document.getElementById('linechart_material'));\n";

		print "chart.draw(data, options);\n";
		print "}\n";
		print "</script>\n";
		print '</head>
			
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
						        print '<li><a href="addaccount.cgi">Add New Account</a></li>';
						        print '<li><a href="logout.cgi">Logout</a></li>';
						        print "<li><a href=\"profile.cgi?id=$getuser\">My Profile</a></li>";
					        } else {
					        	print '<li><a href="login.cgi">Login</a></li>';
					        }
					      print '<li><a href="contact.cgi">Contact iAukaat Team</a></li></ul>
					    </div>
					</td>
				</tr>
				<tr><td><div id="linechart_material"></div></td></tr>
			</table>';
			
		$sth = $dbh->prepare("select tid,date,time, amount, account, prev_value, new_value, type, category, tags,comment from transactioninfo where userid='$getuser' ORDER BY tid DESC");
		$sth->execute();
		
		print "<table align=\"center\" width=\"65%\"><tr style=\"background-color: #D94E67;color: white;\"><th>Transaction ID</th><th>Time</th><th>Account</th><th>Amount</th><th>Type</th><th>Comment</th><th>Category</th><th>Tags</th></tr>";
		
		while (my $ref = $sth->fetchrow_hashref()) {
			my @values = split(',', $ref->{'tags'});
			my $pres = 0;
			foreach my $val (@values) {
				if ($val eq $tagss) {
					$pres = 1;
					break;
				}
			}
			if ($pres == 0) {
				next;
			}
			my $line = "";
			if ($ref->{'type'} eq "Income") {
				$line = "background-color: green;color: black;";
			} else {
				$line = "background-color: #ff5050;color: black;";
			}
			print "<tr style=\"$line\"><td>$ref->{'tid'}</td><td>$ref->{'date'} $ref->{'time'}</td><td><a href=\"byaccount.cgi?id=$ref->{'account'}\" target=\"_blank\">$ref->{'account'}</a></td><td>$ref->{'amount'}</td><td><a href=\"bytype.cgi?id=$ref->{'type'}\" target=\"_blank\">$ref->{'type'}</a></td><td>$ref->{'comment'}</td><td><a href=\"bycategory.cgi?id=$ref->{'category'}\" target=\"_blank\">$ref->{'category'}</a></td>";
			print "<td>";
			foreach my $val (@values) {
				print "<a href=\"bytags.cgi?id=$val\" target=\"_blank\">$val</a>\n";
			}
			print "</td></tr>";
		}
			
		print '</table></body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';
}

1;