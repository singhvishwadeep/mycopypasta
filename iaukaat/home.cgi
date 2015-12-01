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

my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
my $dbh = DBI->connect($dsn,"root","");
my $ip = $ENV{REMOTE_ADDR};
my $info = $ENV{HTTP_USER_AGENT};
my $sth = $dbh->prepare("select ip,count from tr_index_ip_track where ip='$ip'");
$sth->execute();
$count = -1;
while (my $ref = $sth->fetchrow_hashref()) {
	$count = $ref->{'count'};
	break;
}
if ($count != -1) {
	$count++;
	$sth = $dbh->prepare("update tr_index_ip_track set count='$count',http_agent='$info',date=NOW() where ip='$ip'");
	$sth->execute();
} else {
	$sth = $dbh->prepare("insert into tr_index_ip_track ( ip,http_agent,date,count ) VALUES ( '$ip','$info', NOW(),'1')");
	$sth->execute();
}
$sth->finish();
$dbh->disconnect();


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
			#wrong password/ some error
			$err = 1;
		}
	}
}

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
			</tr>
			<tr>
				<td>
				<p>iAukaat. The internet is eating your memory, but something better is taking its place</p> 
				<p>Your money is a huge part of your life. It can determine what you can do and where you can go. Learning how to 
				manage your money the right way is an important step toward taking control of your life.
					Understand where your money is coming from, where it\'s going to, and how to make sure that the way you manage 
					your money falls in line with the values that matter most to you.</p>
					<p>As soon as you start spending your own money, it’s time to start tracking your spending so that you can create 
					and follow a personal budget. Tracking your spending, while sometimes tedious, is the best way to find out exactly 
					where your money is going.
					The simplest way to track your spending, especially your cash, is the low-tech way, with a notebook and a pen. 
					By carrying around the notebook with you, you can track exactly where every dollar is going–from a small coffee on 
					your way to work to a spending splurge at the mall. If you’d prefer, on a daily or weekly basis, you can transfer 
					your handwritten notes to a computer spreadsheet.
					Once you have collected information for about a month, you’ll have a good baseline of information to use to create 
					your personal budget. Some major categories that you’ll want to include are housing, utilities, insurance, food 
					(groceries and dining out), gasoline, clothing, entertainment, and “other". Using a spreadsheet program (such as Excel),
					online service, or other personal finance program, add up the expenses that you’ve been tracking, and then calculate 
					what you’d like to budget for each category. Keep in mind that you’ll need to budget for some items, like gifts and 
					automobile repairs, which will be necessary but won’t occur every month. You can either create a budget for each 
					individual month, with variances for irregular expenses (e.g., heating expenses which will be higher in winter months, 
					or car repairs and gifts), or a standard monthly budget where you include an average amount for expenses such as car 
					repairs, heating, and gifts.
					Your budget should also contain some personal savings amounts for retirement savings, college savings, an emergency fund, 
					long-term savings, and any other savings goals you may have. Don’t wait until the end of the month to see what’s left–budget 
					for your savings first.
					Creating the budget is a good first step, but the most important thing is to follow the budget. Make time weekly or 
					monthly to track your spending, and start to see if you are actually keeping to your budget. Using a personal finance
					program or an online service is probably the easiest way to do this on an ongoing basis, but make sure you continue 
					to track where your cash is going. You could also use this simple Budget Worksheet. You may be surprised to find out 
					how the frequent small amounts you spend actually add up to big money.
					After tracking your personal budget, you may notice some areas where you’ll have to make changes. Don’t just increase 
					your budget without considering alternatives. While you may have no choice, if prices or expenses go up, shop for 
					better deals before giving in to the extra expenses.</p>
				<p>We are also working on some other projects like pathway traversing tool in C and C++ and Note Copy Paste Tool &quot;My Copy-Pasta&quot;. 
				If anyone interested to work in the projects can contact for the same anytime to 
				<a href="mailto:myblueskylabs@gmail.com?Subject=Hello%20My%20Copy%20Pasta%20Team" target="_top">myblueskylabs@gmail.com</a>. 
				 
                <div class="fb-comments" data-href="http://iaukaat.myartsonline.com/" data-numposts="100"></div>
				</td>
			</tr>
		</table>
	</body>
	<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
	<hr width="65%">
	<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
</html>';

1;