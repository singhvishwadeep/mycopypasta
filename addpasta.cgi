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
	my $url="login.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
} else {


	print '<html lang="en-US">
		<head>
			<title>My Copy-Pasta</title>
			<link rel="shortcut icon" href="images/newlogo.ico">
			<link rel="stylesheet" type="text/css" href="css/style.css">
			<link rel="stylesheet" type="text/css" href="css/viewstyle.css">
			<link rel="stylesheet" type="text/css" href="css/addpasta.css">
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
			</table>';
			
			print '<section class="adddata">
				<div class="loginbox">Add Copy-Pasta</div>
				<form action="adddone.cgi" method="post">
				<text class="fontdec">Category&nbsp; </text><select id="selectcategory" name="selectcategory" onChange="changetextbox();"><option selected value="Create New Category">Create New Category</option>';
				
			my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
			my $dbh = DBI->connect($dsn,"root","");
			my $sth = $dbh->prepare("SELECT distinct(category) FROM categoryinfo");
			$sth->execute();
			while (my $ref = $sth->fetchrow_hashref()) {
				if ($ref->{'category'} ne "") {
					print " <option value=\"$ref->{'category'}\">$ref->{'category'}</option>";
				}
			}
			print '</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input required type="text" title="New_Category" placeholder="New Category (max 128 characters)" id="new_category" name="new_category" maxlength="128"/><br /><br />
			    	<text class="fontdec">Topic</text>
			    	<input type="text" required title="Topic" placeholder="Topic (max 256 characters)" style="width:100%" name="topic" maxlength="256"><br /><br />
			    	<text class="fontdec">Discussion</text>
			    	<textarea placeholder="Write your Copy-Pasta! (max 1024 chars)" class="discussion" name="discussion" maxlength="1024"></textarea><br /><br />
			    	<text class="fontdec">Sources</text>
			    	<input type="text" title="Sources" placeholder="Sources (comma separated, max 512 characters)" style="width:100%" name="sources" maxlength="512"><br /><br />
			    	<text class="fontdec">Tags</text>
			    	<input type="text" title="Tags" placeholder="Tags (comma separated, max 256 characters)" style="width:100%" name="tags" maxlength="256"><br /><br />
			    	<text class="fontdec">Share&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</text> <select name="share">
			    	<option value="public">public</option>
			    	<option selected value="private">private</option>
			    	</select><br /><br />
			    	<input type="submit" class="submitbox" name="submit" alt="search" value="Submit your Copy-Pasta">
			    </form>
			</section>
		</body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">©2015 My Blue Sky Labs, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';
}

1;