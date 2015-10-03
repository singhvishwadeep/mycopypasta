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

#if ($login == 0) {
#	my $url="login.cgi";
#	my $t=0; # time until redirect activates
#	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
#	die;
#}

print '<html lang="en-US">
	<head>
		<title>My Copy-Pasta</title>
		<link rel="shortcut icon" href="images/newlogo.ico">
		<link rel="stylesheet" type="text/css" href="css/style.css">
		<link rel="stylesheet" type="text/css" href="css/viewstyle.css">
		<link rel="stylesheet" type="text/css" href="css/paragraph.css">
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
		    document.getElementById("searchcategory").disabled=\'\';
			if (document.getElementById("selectcategory").value != "Keyword for Category") {
			    document.getElementById("searchcategory").disabled=\'true\';
			} else {
			    document.getElementById("searchcategory").disabled=\'\';
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
			<div class="loginbox">Search Copy-Pasta <font color=blue size=2>(Comma will be treated as OR)</font></div>
			<form action="searchwild.cgi" method="post">
				<text class="fontdec" style="font-size: 18px; font-weight: bold;">Wild search Key</text><br/>
		    	<input type="text" title="Wild Search Key" placeholder="Wild Search Key (comma separated for multi keys)" style="width:100%" name="wildkey" maxlength="256">
		    	<input type="checkbox" name="global" value="global" checked="checked">Global Search<br />
		    	<br />
		    	<input type="submit" class="submitbox" name="submit" alt="search" value="Wild Keyword Search">
			</form>
			<hr width="100%" noshade style="color: skyblue;background-color: skyblue;height: 5px;border: 0;">
			
			<form action="searchbyid.cgi" method="post">
				<text class="fontdec" style="font-size: 18px; font-weight: bold;">Search by ID</text><br/>
		    	<input type="text" title="Search by ID" placeholder="Copy Pasta ID (comma separated for multiple IDs)" style="width:100%" name="idkey" maxlength="256">
		    	<input type="checkbox" name="global" value="global" checked="checked">Global Search<br />
		    	<br />
		    	<input type="submit" class="submitbox" name="submit" alt="search" value="ID Keyword Search">
			</form>
			<hr width="100%" noshade style="color: skyblue;background-color: skyblue;height: 5px;border: 0;">
			
			<form action="searchadvance.cgi" method="post">
			<text class="fontdec" style="font-size: 18px; font-weight: bold;">Advance Search</text><br/><br/>
			<text class="fontdec">Search Category&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</text><select id="selectcategory" name="selectcategory" onChange="changetextbox();"><option selected value="Keyword for Category">Keyword for Category</option>';
			
		my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
		my $dbh = DBI->connect($dsn,"root","");
		my $sth = $dbh->prepare("SELECT distinct(category) FROM categoryinfo");
		$sth->execute();
		while (my $ref = $sth->fetchrow_hashref()) {
			if ($ref->{'category'} ne "") {
				print " <option value=\"$ref->{'category'}\">$ref->{'category'}</option>";
			}
		}
		print '</select>&nbsp;&nbsp;<text class="fontdec">OR&nbsp;&nbsp;&nbsp;</text><input type="text" title="searchcategory" placeholder="Category Keys (comma separated for multi keys)" id="searchcategory" name="searchcategory" maxlength="128"/><br /><br />
		    	<text class="fontdec">Search Topic&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </text>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="text" title="searchtopic" placeholder="Topic Keys (comma separated for multi keys)" id="searchtopic" name="searchtopic" maxlength="128"/><br /><br />
		    	<text class="fontdec">Search Discussion&nbsp; </text>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="text" title="searchdiscussion" placeholder="Discussion Keys (comma separated for multi keys)" id="searchdiscussion" name="searchdiscussion" maxlength="128"/><br /><br />
		    	<text class="fontdec">Search Sources&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </text>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="text" title="searchsources" placeholder="Source Keys (comma separated for multi keys)" id="searchsources" name="searchsources" maxlength="128"/><br /><br />
		    	<text class="fontdec">Search Tags&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</text><select id="selecttags" name="selecttags" onChange="changetextbox();"><option selected value="Keyword for Tags">Keyword for Tags</option>';
			
		$sth = $dbh->prepare("SELECT distinct(tag) FROM taginfo");
		$sth->execute();
		while (my $ref = $sth->fetchrow_hashref()) {
			if ($ref->{'tag'} ne "") {
				print " <option value=\"$ref->{'tag'}\">$ref->{'tag'}</option>";
			}
		}
		print '</select>&nbsp;&nbsp;<text class="fontdec">OR&nbsp;&nbsp;&nbsp;</text><input type="text" title="searchtags" placeholder="Tags Keys (comma separated for multi keys)" id="searchtags" name="searchtags" maxlength="128"/><br /><br />
		    	<input type="checkbox" name="global" value="global" checked="checked">Global Search<br />
		    	<br />
		    	<input type="submit" class="submitbox" name="submit" alt="search" value="Advance Keyword Search">
		    </form>
		</section></body>
	<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">©2015 My Blue Sky Labs, powered by Vishwadeep Singh</text></div>
	<hr width="65%">
	<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
</html>';


1;