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
	my $getuser = $session->param('logged_in_userid_mycp');
	my $getusername = $session->param('logged_in_user_mycp');
	
	my $account=param('account');
	my $ttype=param('ttype');
	my $balance=param('balance');
	
	$account = trim($account);
	$ttype = trim($ttype);
	$balance = trim($balance);
	
	$account =~ s{\'}{\\'}g;
	$ttype =~ s{\'}{\\'}g;
	$balance=~ s{\'}{\\'}g;
	
	if ($account ne "") {
		
		my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
		my $dbh = DBI->connect($dsn,"root","");
		
		my $sth = $dbh->prepare("SELECT account,userid FROM traccountinfo where userid='$getuser' AND account='$account'");
		$sth->execute();
		my $catid = -1;
		while (my $ref = $sth->fetchrow_hashref()) {
			$catid = 0;
		}
		
		if ($catid == 0) {
			my $url="addaccount.cgi";
			my $t=0; # time until redirect activates
			print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
		} else {
			# new category found for a user
			my $balancen = 0.0;
			if ($balance ne "") {
				$balancen = $balance;
			}
			$sth = $dbh->prepare("INSERT into traccountinfo ( account,userid,type,balance ) VALUES ( '$account','$getuser', '$ttype', '$balancen')");
			$sth->execute();
			
			if ($balancen != 0.0) {
				$tagcount = 0;
				$tagid = -1;
				$sth = $dbh->prepare("SELECT id,tag,tag_count,userid FROM trtaginfo where userid='$getuser' AND tag='initial input'");
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
					$tagcount++;
					$sth = $dbh->prepare("update trtaginfo set tag_count='$tagcount' where id='$tagid'\n");
				} else {
					# new category found for a user
					$sth = $dbh->prepare("INSERT into trtaginfo ( tag,tag_count,userid ) VALUES ( 'initial input','1', '$getuser')");
				}
				$sth->execute();
				
				$sth = $dbh->prepare("SELECT id,category,category_count,userid FROM trcategoryinfo where userid='$getuser' AND category='initial input'");
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
					$catcount++;
					$sth = $dbh->prepare("update trcategoryinfo set category_count='$catcount' where id='$catid'");
				} else {
					# new category found for a user
					$sth = $dbh->prepare("INSERT into trcategoryinfo ( category,category_count,userid ) VALUES ( 'initial input','1', '$getuser')");
				}
				$sth->execute();
				
				my $ip = $ENV{REMOTE_ADDR};
				my $info = $ENV{HTTP_USER_AGENT};
				$sth = $dbh->prepare("INSERT into transactioninfo ( date,time,userid,amount,account,prev_value,new_value,type,category,tags,ip,http_agent, comment ) VALUES ( CURDATE(), CURTIME(), '$getuser','$balancen', '$account','0.0', '$balancen', 'Income','initial input','initial input','$ip','$info', 'initial input')");
				$sth->execute();
				$sth->finish();
				$dbh->disconnect();
				$url = "addaccount.cgi";
				my $t=0; # time until redirect activates
				print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
				
			} else {
				my $url="addaccount.cgi";
				my $t=0; # time until redirect activates
				print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
			}
		}
	} else {
		my $url="addaccount.cgi";
		my $t=0; # time until redirect activates
		print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
	}
}
1;