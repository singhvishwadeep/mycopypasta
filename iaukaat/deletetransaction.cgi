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

sub  trim { 
	my $s = shift;
	$s =~ s/^\s+|\s+$//g;
	return $s;
}

if ($login == 1) {

	my $editid = $q->param('id');
	
	if (looks_like_number($editid)) {
	  
	} else {
		$editid = 0;
	}
	
	my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
	my $dbh = DBI->connect($dsn,"root","");
	my $getuser = $session->param('logged_in_userid_mycp');
	my $getusername = $session->param('logged_in_user_mycp');
	
	my $tags = "";
	my $category = "";
	
	my $sth = $dbh->prepare("select tags,category from transactioninfo where userid='$getuser' AND tid='$editid'");
	$sth->execute();
	while (my $ref = $sth->fetchrow_hashref()) {
		$category = $ref->{'category'};
		$tags = $ref->{'tags'};
		break;
	}
	
	if ($category ne "") {
		$sth = $dbh->prepare("SELECT id,category,category_count,userid FROM trcategoryinfo where userid='$getuser' AND category='$category'");
		$sth->execute();
		my $catcount = 0;
		my $catid = -1;
		while (my $ref = $sth->fetchrow_hashref()) {
			if ($ref->{'category'} ne "") {
				$catid = $ref->{'id'};
				$catcount = $ref->{'category_count'};
				break;
			}
		}
		if ($catid != -1) {
			# prev category exists for a user
			$catcount--;
			$sth = $dbh->prepare("update trcategoryinfo set category_count='$catcount' where id='$catid'");
		}
	}
	
	if ($tags ne "") {
		my @valtags = split(',', $tags);
		foreach my $val (@valtags) {
			$val = trim($val);
			if ($val ne "") {
				$tagcount = 0;
				$tagid = -1;
				$sth = $dbh->prepare("SELECT id,tag,tag_count,userid FROM trtaginfo where userid='$getuser' AND tag='$val'");
				$sth->execute();
				while (my $ref = $sth->fetchrow_hashref()) {
					if ($ref->{'tag'} ne "") {
						$tagid = $ref->{'id'};
						$tagcount = $ref->{'tag_count'};
						break;
					}
				}
				if ($tagid != -1) {
					# prev tag exists for a user
					$tagcount--;
					$sth = $dbh->prepare("update trtaginfo set tag_count='$tagcount' where id='$tagid'\n");
				}
				$sth->execute();
			}
		}
	}
	
	$sth = $dbh->prepare("delete from transactioninfo where tid='$editid' and userid='$getuser'");
	$sth->execute();
	$sth->finish();
	$dbh->disconnect();
	my $url="view.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
}


1;