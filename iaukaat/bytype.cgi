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
		} else {
			my $url="login.cgi";
			my $t=0; # time until redirect activates
			print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
		}
	}
}

my $ttype = $q->param('id');

if ($login && $ttype ne "") {
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
			my $sth = $dbh->prepare("select amount,date from transactioninfo where userid='$getuser' AND type='$ttype' ORDER BY tid ASC");
			$sth->execute();
			my %data;
			my @refarr;
			while (my $ref = $sth->fetchrow_hashref()) {
				if( exists($data{$ref->{'date'}}) ){
					$data{$ref->{'date'}} =  $data{$ref->{'date'}} + $ref->{'amount'};
				} else{
					push(@refarr, $ref->{'date'});
					$data{$ref->{'date'}} = $ref->{'amount'};
				}
			}		
			
			print "<script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>\n";
			print "<script type=\"text/javascript\">\n";
			print "google.load('visualization', '1.1', {packages: ['line']});\n";
			print "google.setOnLoadCallback(drawChart);\n";
			print "function drawChart() {\n";
	
			print "var data = new google.visualization.DataTable();\n";
			print "data.addColumn('number', 'Days');\n";
			print "data.addColumn('number', 'Balance');\n";
	
			print "data.addRows([\n";
			my $i = 0;
			foreach my $i (0 .. $#refarr) {
				if ($i != $#refarr) {
					print "[$i,$data{$refarr[$i]}],\n";
				} else {
					print "[$i,$data{$refarr[$i]}]\n";
				}
			}
			print "]);\n";
			
			print "var options = {\n";
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
				<tr><td><div id="linechart_material"></div></td></tr>
			</table>';
			
		$sth = $dbh->prepare("select tid,date,time, amount, account, prev_value, new_value, type, category, tags,comment from transactioninfo where userid='$getuser' AND type='$ttype' ORDER BY tid DESC");
		$sth->execute();
		
		print "<table align=\"center\" width=\"65%\"><tr style=\"background-color: #D94E67;color: white;\"><th>Tr ID</th><th>Time</th><th>Account</th><th>Amount</th><th>Balance</th><th>Type</th><th>Comment</th><th>Category</th><th>Tags</th></tr>";
		
		my $io = 0;
		
		while (my $ref = $sth->fetchrow_hashref()) {
			my $line = "";
			if ($io == 0) {
				$io = 1;
				$line = "background-color: #ff5050;color: white;";
			} else {
				$io = 0;
				$line = "background-color: #999966;color: white;";
			}
			print "<tr style=\"$line\"><td>$ref->{'tid'}</td><td>$ref->{'date'} $ref->{'time'}</td><td><a href=\"byaccount.cgi?id=$ref->{'account'}\" target=\"_blank\">$ref->{'account'}</a></td><td>$ref->{'amount'}</td><td>$ref->{'new_value'}</td><td><a href=\"bytype.cgi?id=$ref->{'type'}\" target=\"_blank\">$ref->{'type'}</a></td><td>$ref->{'comment'}</td><td><a href=\"bycategory.cgi?id=$ref->{'category'}\" target=\"_blank\">$ref->{'category'}</a></td><td><a href=\"bytags.cgi?id=$ref->{'tags'}\" target=\"_blank\">$ref->{'tags'}</a></td></tr>";
		}
			
		print '</table></body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';
}

1;