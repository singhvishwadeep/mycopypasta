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
	
	my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
	my $dbh = DBI->connect($dsn,"root","");
	
	
	if ($selectcategory eq "Create New Category") {
		if ($new_category ne "") {
			$category = $new_category;
		} else {
			$category = "general";
		}
	} else {
		$category = $selectcategory;
	}
	
	my $sth = $dbh->prepare("SELECT id,category,count,userid FROM categoryinfo where userid='$getuser' AND category='$category'");
	$sth->execute();
	my $catcount = 0;
	my $catid = -1;
	while (my $ref = $sth->fetchrow_hashref()) {
		if ($ref->{'category'} ne "") {
			$catid = $ref->{'id'};
			$catcount = $ref->{'count'};
			break;
		}
	}
	
	if ($catid != -1) {
		# prev category exists for a user
		$catcount++;
		$sth = $dbh->prepare("update categoryinfo set count='$catcount' where id='$catid'");
	} else {
		# new category found for a user
		$sth = $dbh->prepare("INSERT into categoryinfo ( category,count,userid ) VALUES ( '$category','1', '$getuser')");
	}
	$sth->execute();
	
	my @parsedsources;
	my @valsources = split(',', $sources);
	foreach my $val (@valsources) {
		$val = trim($val);
		push @parsedsources, $val;
	}
	$sources = join ( ',', @parsedsources );
	my @parsedtags;
	my @valtags = split(',', $tags);
	my $tagcount = 0;
	my $tagid = -1;
	foreach my $val (@valtags) {
		$val = trim($val);
		if ($val ne "") {
			push @parsedtags, $val;
			$tagcount = 0;
			$tagid = -1;
			$sth = $dbh->prepare("SELECT id,tag,tagcount,userid FROM taginfo where userid='$getuser' AND tag='$val'");
			$sth->execute();

			while (my $ref = $sth->fetchrow_hashref()) {
				if ($ref->{'tag'} ne "") {
					$tagid = $ref->{'id'};
					$tagcount = $ref->{'tagcount'};
					break;
				}
			}
			
			if ($tagid != -1) {
				# prev tag exists for a user
				$tagcount++;
				$sth = $dbh->prepare("update taginfo set tagcount='$tagcount' where id='$tagid'\n");
			} else {
				# new category found for a user
				$sth = $dbh->prepare("INSERT into taginfo ( tag,tagcount,userid ) VALUES ( '$val','1', '$getuser')");
			}
			$sth->execute();
		}
	}
	$tags = join ( ',', @parsedtags );
	if ($share eq "private") {
		$share = 0;
	} else {
		$share = 1;
	}

	$sth = $dbh->prepare("INSERT into datasubmission ( user,username,category,topic,discussion,source,tags,date,public,showme ) VALUES ( '$getuser','$getusername', '$category','$topic','$discussion','$sources','$tags',NOW(),'$share','1')");
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