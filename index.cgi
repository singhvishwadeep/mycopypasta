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
my $sth = $dbh->prepare("select ip,count from index_ip_track where ip='$ip'");
$sth->execute();
$count = -1;
while (my $ref = $sth->fetchrow_hashref()) {
	$count = $ref->{'count'};
	break;
}
if ($count != -1) {
	$count++;
	$sth = $dbh->prepare("update index_ip_track set count='$count',http_agent='$info',date=NOW() where ip='$ip'");
	$sth->execute();
} else {
	$sth = $dbh->prepare("insert into index_ip_track ( ip,http_agent,date,count ) VALUES ( '$ip','$info', NOW(),'1')");
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
		<title>My Copy-Pasta</title>
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
			</tr>
			<tr>
				<td>
				<p>My Copy-Pasta. The internet is eating your memory, but something better is taking its place</p> 
				<p>You sometime wishes, you could paste and save your copied information.</p>
				<p>This creation is inspired by several thoughts. It is the idea of ideas. In the years since the world started going digital, 
				one of the big changes has been that we don’t need to remember very much. As we come across with different information daily, but, we 
				donot keep track of them. You cannot trust on human mind for storing the information for longer time. Here, we are providing you this 
				platform
				so that you can save your information like daily find outs, logics in your own words and understanding, important web links or bookmarks, 
				important programming syntaxes/uses, manuals, definitions, important dates, and many other things.</p>
				
				<p>In my lifetime I had seen lot of branches of science 
				and still dealing with different dimensions of problems, 
				which makes me learn new things daily. But, slowly I start forgetting those solutions and loosing track of them. Hence, I thought of 
				building a platform, where you can save anything you want and keep it for future purpose.</p>
				<p>This tool is written in cgi-perl from scratch and is done in 2 weeks of time frame. For usage, you need to <a href="register.cgi">register</a> 
				with proper username and password. After logging in, you can add your copy-pasta with proper topic and discussion with sources and tags.
				This will be saved as proper id, which can only be accesed by your account. There is an option to save your copy-pasta 
				in private/public set also, in which private is by default. 
				Private set can only be accessed by you only, whereas public set can be accessed by any one. After saving your information, you can also
				search them in future by wild card search, or directly ID search, or advance search with lot of parameters.
				More organised you save, better search results you will get.</p>
				<p>We are also working on some other projects like pathway traversing tool in C and C++ and Money Management Tool 
				(named &quot;Aukaat&quot;) 
				in cgi-perl. If anyone interested to work in the projects can contact for the same anytime to 
				<a href="mailto:myblueskylabs@gmail.com?Subject=Hello%20My%20Copy%20Pasta%20Team" target="_top">myblueskylabs@gmail.com</a>. 
				 
                <div class="fb-comments" data-href="http://mycopypasta.myartsonline.com/" data-numposts="100"></div>
				</td>
			</tr>
		</table>
	</body>
	<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">&copy;2015 <a href="mailto:myblueskylabs@gmail.com ?Subject=Reg:Hello" target="_top">My Blue Sky Labs (myblueskylabs@gmail.com)</a>, powered by Vishwadeep Singh</text></div>
	<hr width="65%">
	<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
</html>';

1;