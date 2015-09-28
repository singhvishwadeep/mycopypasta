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
}

sub  trim { 
	my $s = shift;
	$s =~ s/^\s+|\s+$//g;
	return $s;
}

my $getuser = $session->param('logged_in_userid_mycp');
my $getusername = $session->param('logged_in_user_mycp');

my $topic=param('topic');
my $selectcategory=param('selectcategory');
my $new_category=param('new_category');
my $discussion=param('discussion');
my $sources=param('sources');
my $tags=param('tags');
my $share=param('share');
my $category = "";

$topic = trim($topic);
$selectcategory = trim($selectcategory);
$new_category = trim($new_category);
$discussion = trim($discussion);
$sources = trim($sources);
$tags = trim($tags);
$share = trim($share);

#print "user = -$getuser- <br/>";
#print "selectcategory = $selectcategory <br>";
#print "new_category = $new_category <br>";
#print "topic = $topic <br>";
#print "discussion = $discussion <br>";
#print "sources = $sources <br>";
#print "tags = $tags <br>";
#print "share = $share <br>";


if ($topic ne "" and $discussion ne "") {
	if ($selectcategory eq "Create New Category") {
		if ($new_category ne "") {
			$category = $new_category;
		} else {
			$category = "general";
		}
	} else {
		$category = $selectcategory;
	}
	my @parsedsources;
	my @valsources = split(',', $sources);
	foreach my $val (@valsources) {
		$val = trim($val);
		push @parsedsources, $val;
	}
	$sources = join ( ',', @parsedsources );
	my @parsedtags;
	my @valtags = split(',', $tags);
	foreach my $val (@valtags) {
		$val = trim($val);
		push @parsedtags, $val;
	}
	$tags = join ( ',', @parsedtags );
	if ($share eq "private") {
		$share = 0;
	} else {
		$share = 1;
	}
	
	
	my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
	my $dbh = DBI->connect($dsn,"root","");
	my $sth = $dbh->prepare("INSERT into datasubmission ( user,username,category,topic,discussion,source,tags,date,public,showme ) VALUES ( '$getuser','$getusername', '$category','$topic','$discussion','$sources','$tags',NOW(),'$share','1')");
	$sth->execute();
	$sth->finish();
	$dbh->disconnect();
	$url = "view.cgi";
} else {
	$url = "addpasta.cgi";
}

my $t=1; # time until redirect activates
print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
1;