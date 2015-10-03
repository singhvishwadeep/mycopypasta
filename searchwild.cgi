#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use DBI;
use HTML::Entities;

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

#if ($login == 0) {
#	my $url="login.cgi";
#	my $t=0; # time until redirect activates
#	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
#} 


my $idkeys = $q->param('wildkey');
my $globalhit = $q->param('global');

$idkeys = trim($idkeys);
$globalhit = trim($globalhit);

if ($globalhit eq "") {
	$globalhit = 0;
} else {
	$globalhit = 1;
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
			</table>
			<table class="box" align="center" width="65%">';
			if ($idkeys ne "") {
				
				if ($login == 1) {
						my $getuser = $session->param('logged_in_userid_mycp');
						my $getusername = $session->param('logged_in_user_mycp');
						my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
						my $dbh = DBI->connect($dsn,"root","");
						my $query = "select id,myusername from userdatabase";
						my $sth = $dbh->prepare($query);
						$sth->execute();
						my %userinfo;
						while (my $ref = $sth->fetchrow_hashref()) {
							$userinfo{$ref->{'myusername'}} = $ref->{'id'};
						}
						
						$query = "SELECT id,username,category,topic,discussion,source,tags,date,public FROM datasubmission where";
						
						if ($globalhit == 1) {
							$query .= " (user='$getuser' OR public=1)";
						} else {
							$query .= " (user='$getuser')";
						}
						
						my @values = split(',', $idkeys);
						$query .= " AND (";
						my $t1 = 0;
						foreach my $val (@values) {
							$val = trim($val);
							$val =~ s{\'}{\\}g;
							if ($t1 == 0) {
								$t1 = 1;
								$query .= "id like '%$val%' OR category like '%$val%' OR topic like '%$val%' OR discussion like '%$val%' OR source like '%$val%' OR tags like '%$val%'";
							} else {
								$query .= " OR id like '%$val%' OR category like '%$val%' OR topic like '%$val%' OR discussion like '%$val%' OR source like '%$val%' OR tags like '%$val%'";
							}
						}
						$query .= ")";
						$query .= " AND showme=1 ORDER BY id DESC";
						$sth = $dbh->prepare($query);
						$sth->execute();
						my $countres = $sth->rows;
						print "<tr><td><a class=\"edit_button\">Found $countres Results</a><br><br></td></tr>";
						my $turn = 0;
						while (my $ref = $sth->fetchrow_hashref()) {
							
							my $id = $ref->{'id'};
							my $category = $ref->{'category'};
							my $topic = $ref->{'topic'};
							my $showuser = $ref->{'username'};
							my $discussion = $ref->{'discussion'};
							my $source = $ref->{'source'};
							my $date = $ref->{'date'};
							my $tags = $ref->{'tags'};
							if ($ref->{'public'} == 0) {
								$shared = "Private";
							} else {
								$shared = "Public";
							}
							print "<tr><td>";
							if ($turn == 0) {
								$turn = 1;
								print "<p class=\"one\">";
							} else {
								$turn = 0;
								print "<p class=\"two\">";
							}
							print '<img src="images/note.jpg" alt="Note View" style="width:20px;height:20px;">';
							print "<a href=\"view.cgi\" class=\"heading_link\"><text class=\"headings\">$id. $topic</text></a><a class=\"edit_button\" href=\"view.cgi\">";
							print '<img src="images/edit.jpg" alt="Edit" style="width:10px;height:10px;padding-right:3px">Edit</a><br>';
							print "<text class=\"date\">$date by <a href=\"profile.cgi?id=$userinfo{$showuser}\" class=\"heading_link\" target=\"_blank\">$showuser</a> (Shared: $shared)</text><br/>";
							my $string = "categoryview.cgi?showmycategory=$category";
							encode_entities($string);
							print "<a class=\"category_button\" href=\"$string\" target=\"_blank\">Category: $category</a><br><br>";
							print "<textarea readonly class=\"discussion\">$discussion</textarea><br>";
							print '<text class="information">Sources:</text>';
							my @values = split(',', $source);
							foreach my $val (@values) {
								$val = trim($val);
								print "<a class=\"source_button\" href=\"$val\">$val</a>&nbsp;";
							}
							print '<br><text class="information">Tags:</text>';
							my @values = split(',', $tags);
							foreach my $val (@values) {
								$val = trim($val);
								my $string = "tagview.cgi?showmytag=$val";
   								encode_entities($string);
								print "<a class=\"tag_button\" href=\"$string\" target=\"_blank\">$val</a>&nbsp;";
							}
							print '<br>
									</p>
								</td>
							</tr>';
						}
					} elsif ($globalhit == 1) {
						my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
						my $dbh = DBI->connect($dsn,"root","");
						my $query = "select id,myusername from userdatabase";
						my $sth = $dbh->prepare($query);
						$sth->execute();
						my %userinfo;
						while (my $ref = $sth->fetchrow_hashref()) {
							$userinfo{$ref->{'myusername'}} = $ref->{'id'};
						}
						
						$query = "SELECT id,username,category,topic,discussion,source,tags,date,public FROM datasubmission where (public=1)";
						
						my @values = split(',', $idkeys);
						$query .= " AND (";
						my $t1 = 0;
						foreach my $val (@values) {
							$val = trim($val);
							$val =~ s{\'}{\\}g;
							if ($t1 == 0) {
								$t1 = 1;
								$query .= "id like '%$val%' OR category like '%$val%' OR topic like '%$val%' OR discussion like '%$val%' OR source like '%$val%' OR tags like '%$val%'";
							} else {
								$query .= " OR id like '%$val%' OR category like '%$val%' OR topic like '%$val%' OR discussion like '%$val%' OR source like '%$val%' OR tags like '%$val%'";
							}
						}
						$query .= ")";
						$query .= " AND showme=1 ORDER BY id DESC";
						$sth = $dbh->prepare($query);
						$sth->execute();
						my $countres = $sth->rows;
						print "<tr><td><a class=\"edit_button\">Found $countres Results</a><br><br></td></tr>";
						my $turn = 0;
						while (my $ref = $sth->fetchrow_hashref()) {
							
							my $id = $ref->{'id'};
							my $category = $ref->{'category'};
							my $topic = $ref->{'topic'};
							my $showuser = $ref->{'username'};
							my $discussion = $ref->{'discussion'};
							my $source = $ref->{'source'};
							my $date = $ref->{'date'};
							my $tags = $ref->{'tags'};
							if ($ref->{'public'} == 0) {
								$shared = "Private";
							} else {
								$shared = "Public";
							}
							print "<tr><td>";
							if ($turn == 0) {
								$turn = 1;
								print "<p class=\"one\">";
							} else {
								$turn = 0;
								print "<p class=\"two\">";
							}
							print '<img src="images/note.jpg" alt="Note View" style="width:20px;height:20px;">';
							print "<a href=\"view.cgi\" class=\"heading_link\"><text class=\"headings\">$id. $topic</text></a><a class=\"edit_button\" href=\"view.cgi\">";
							print '<img src="images/edit.jpg" alt="Edit" style="width:10px;height:10px;padding-right:3px">Edit</a><br>';
							print "<text class=\"date\">$date by <a href=\"profile.cgi?id=$userinfo{$showuser}\" class=\"heading_link\" target=\"_blank\">$showuser</a> (Shared: $shared)</text><br/>";
							my $string = "categoryview.cgi?showmycategory=$category";
							encode_entities($string);
							print "<a class=\"category_button\" href=\"$string\" target=\"_blank\">Category: $category</a><br><br>";
							print "<textarea readonly class=\"discussion\">$discussion</textarea><br>";
							print '<text class="information">Sources:</text>';
							my @values = split(',', $source);
							foreach my $val (@values) {
								$val = trim($val);
								print "<a class=\"source_button\" href=\"$val\">$val</a>&nbsp;";
							}
							print '<br><text class="information">Tags:</text>';
							my @values = split(',', $tags);
							foreach my $val (@values) {
								$val = trim($val);
								my $string = "tagview.cgi?showmytag=$val";
   								encode_entities($string);
								print "<a class=\"tag_button\" href=\"$string\" target=\"_blank\">$val</a>&nbsp;";
							}
							print '<br>
									</p>
								</td>
							</tr>';
						}
					} else {
						print "<tr><td><a class=\"edit_button\">Found 0 Results</a><br><br></td></tr>";
					}
			} else {
				print "<tr><td><font color=\"red\">Nothing recieved</font></td></tr>";
			}
			
		print '</table>
		</body>
		<div style="text-align:center"><text style="color:grey;font-size:12px;font:status-bar">©2015 My Blue Sky Labs, powered by Vishwadeep Singh</text></div>
		<hr width="65%">
		<div style="text-align:center"><div class="fb-follow" data-href="https://www.facebook.com/vsdpsingh" data-width="250" data-height="250" data-layout="standard" data-show-faces="true"></div></div>
	</html>';

1;