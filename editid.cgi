#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use DBI;
use HTML::Entities;
use Scalar::Util qw(looks_like_number);

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

sub  trim { 
	my $s = shift;
	$s =~ s/^\s+|\s+$//g;
	return $s;
}

if ($login == 0) {
	my $url="login.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
} else {

	my $editid = $q->param('id');
	
	if (looks_like_number($editid)) {
	  
	} else {
		$editid = 0;
	}
	
	my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
	my $dbh = DBI->connect($dsn,"root","");
	my $getuser = $session->param('logged_in_userid_mycp');
	my $getusername = $session->param('logged_in_user_mycp');
	
	my $edituserid = -1;
	my $query = "select user from datasubmission where id='$editid' AND showme=1";
	my $sth = $dbh->prepare($query);
	$sth->execute();
	while (my $ref = $sth->fetchrow_hashref()) {
		$edituserid = $ref->{'user'};
		break;
	}
	if ($edituserid == $getuser) {
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
							        print '<li><a href="logout.cgi">Logout</a></li>
							        <li><a href="profile.cgi">Profile</a></li>';
						        } else {
						        	print '<li><a href="login.cgi">Login</a></li>';
						        }
						      print '</ul>
						    </div>
						</td>
					</tr>
				</table>';
					
					my $query = "select id,myusername from userdatabase";
					my $sth = $dbh->prepare($query);
					$sth->execute();
					my %userinfo;
					while (my $ref = $sth->fetchrow_hashref()) {
						$userinfo{$ref->{'myusername'}} = $ref->{'id'};
					}
					
					$query = "SELECT id,username,category,topic,discussion,source,tags,date,public FROM datasubmission where user='$getuser' AND showme=1 AND id='$editid'";
					$sth = $dbh->prepare($query);
					$sth->execute();
					my $id = "";
					my $category = "";
					my $topic = "";
					my $showuser = "";
					my $discussion = "";
					my $source = "";
					my $tags = "";
					my $date = "";
					my $shared = "";
					
					
					while (my $ref = $sth->fetchrow_hashref()) {
						$id = $ref->{'id'};
						$category = $ref->{'category'};
						$topic = $ref->{'topic'};
						$showuser = $ref->{'username'};
						$discussion = $ref->{'discussion'};
						$source = $ref->{'source'};
						$tags = $ref->{'tags'};
						$date = $ref->{'date'};
						if ($ref->{'public'} == 0) {
							$shared = "Private";
						} else {
							$shared = "Public";
						}
						break;
					}
					
					print '<section class="adddata">
				<div class="loginbox">Edit Copy-Pasta</div>
				<form action="updateedit.cgi" method="post">
				<text class="fontdec">ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </text><input required type="text" name="id" ';
				print "value=\"$id\" style=\"width:30%;background:grey\" readonly/><br /><br />";
				print '<text class="fontdec">Category&nbsp; </text><select id="selectcategory" name="selectcategory" onChange="changetextbox();"><option value="Create New Category">Create New Category</option>';
				
				$sth = $dbh->prepare("SELECT distinct(category) FROM categoryinfo");
				$sth->execute();
				while (my $ref = $sth->fetchrow_hashref()) {
					if ($ref->{'category'} ne "") {
						my $op = "";
						if ($category eq $ref->{'category'}) {
							$op = "selected";
						}
						print " <option $op value=\"$ref->{'category'}\">$ref->{'category'}</option>";
					}
				}
				print "</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input required type=\"text\" title=\"new_category\" placeholder=\"New Category (max 128 characters)\" id=\"new_category\" name=\"new_category\" maxlength=\"128\" disabled/><br /><br />
			    	<text class=\"fontdec\">Topic</text>
			    	<input type=\"text\" required title=\"Topic\" placeholder=\"Topic (max 256 characters)\" style=\"width:100%\" name=\"topic\" value=\"$topic\" maxlength=\"256\"><br /><br />
			    	<text class=\"fontdec\">Discussion</text>
			    	<textarea placeholder=\"Write your Copy-Pasta! (max 1024 chars)\" class=\"discussion\" name=\"discussion\" maxlength=\"1024\" >$discussion</textarea><br /><br />
			    	<text class=\"fontdec\">Sources</text>
			    	<input type=\"text\" title=\"Sources\" placeholder=\"Sources (comma separated, max 512 characters)\" style=\"width:100%\" name=\"sources\" maxlength=\"512\" value=\"$source\"><br /><br />
			    	<text class=\"fontdec\">Tags</text>
			    	<input type=\"text\" title=\"Tags\" placeholder=\"Tags (comma separated, max 256 characters)\" style=\"width:100%\" name=\"tags\" maxlength=\"256\" value=\"$tags\"><br /><br />
			    	<text class=\"fontdec\">Share&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</text> <select name=\"share\">";
				
				if ($shared eq "Public") {
					print "<option selected value=\"public\">public</option>";
					print "<option value=\"private\">private</option>";
				} else {
					print "<option value=\"public\">public</option>";
					print "<option selected value=\"private\">private</option>";
				}
				
				print "</select><br /><br />
			    	<input type=\"submit\" class=\"submitbox\" name=\"submit\" alt=\"search\" value=\"Update your Copy-Pasta\">
			    </form>
			</section>";
					
				print '</body>
			<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">©2015 My Blue Sky Labs, powered by Vishwadeep Singh</text></div>
			<hr width="65%">
			<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
		</html>';
	}

}
1;