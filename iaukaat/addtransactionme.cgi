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

sub  trim { 
	my $s = shift;
	$s =~ s/^\s+|\s+$//g;
	return $s;
}

if ($login == 0) {
	my $url="login.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
} else{
	my $getuser = $session->param('logged_in_userid_mycp');
	my $getusername = $session->param('logged_in_user_mycp');
	
	my $amount=param('amount');
	my $ttype=param('ttype');
	my $account=param('selectaccount');
	my $selectcategory=param('selectcategory');
	my $New_Category=param('new_category');
	my $tags=param('tags');
	my $comment=param('comment');
	my $category = "";
	
	$amount = trim($amount);
	$ttype = trim($ttype);
	$account = trim($account);
	$selectcategory = trim($selectcategory);
	$New_Category = trim($New_Category);
	$tags = trim($tags);
	$comment = trim($comment);
	
	$amount =~ s{\'}{\\'}g;
	$ttype =~ s{\'}{\\'}g;
	$account=~ s{\'}{\\'}g;
	$selectcategory =~ s{\'}{\\'}g;
	$New_Category =~ s{\'}{\\'}g;
	$tags =~ s{\'}{\\'}g;
	$comment =~ s{\'}{\\'}g;
	
	if ($amount ne "" && $account ne "") {
		
		my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
		my $dbh = DBI->connect($dsn,"root","");
		
		
		if ($selectcategory eq "Create New Category") {
			if ($new_category ne "") {
				$category = $new_category;
			} else {
				$category = "pocket purse";
			}
		} else {
			$category = $selectcategory;
		}
		
		if ($category eq "") {
			$category = "pocket purse";
		}
		
		my $sth = $dbh->prepare("SELECT id,category,category_count,userid FROM trcategoryinfo where userid='$getuser' AND category='$category'");
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
			$sth = $dbh->prepare("INSERT into trcategoryinfo ( category,category_count,userid ) VALUES ( '$category','1', '$getuser')");
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
					$tagcount++;
					$sth = $dbh->prepare("update trtaginfo set tag_count='$tagcount' where id='$tagid'\n");
				} else {
					# new category found for a user
					$sth = $dbh->prepare("INSERT into trtaginfo ( tag,tag_count,userid ) VALUES ( '$val','1', '$getuser')");
				}
				$sth->execute();
			}
		}
		$tags = join ( ',', @parsedtags );
		
		$sth = $dbh->prepare("SELECT type,balance,id FROM traccountinfo where userid='$getuser' AND account='$account'");
		$sth->execute();
		my $trbalance = 0;
		my $trid = -1;
		my $trtype = "";
		while (my $ref = $sth->fetchrow_hashref()) {
			$trid = $ref->{'id'};
			$trtype = $ref->{'type'};
			$trbalance = $ref->{'balance'};
			break;
		}
		my $prev_amount = $trbalance;
		my $new_amount = $trbalance;
		if ($trid != -1) {
			my $ip = $ENV{REMOTE_ADDR};
			my $info = $ENV{HTTP_USER_AGENT};
			
			if ($trtype eq "credit") {
				# going in credit card
				if ($ttype eq "Expence") {
					# spent from credit card
					$new_amount = $new_amount + $amount;
				} else {
					#  added to credit card
					$new_amount = $new_amount - $amount;
				}
			} else {
				if ($ttype eq "Expence") {
					# spent from debit
					$new_amount = $new_amount - $amount;
				} else {
					#  added to debit
					$new_amount = $new_amount + $amount;
				}
			}
			$sth = $dbh->prepare("update traccountinfo set balance='$new_amount' where userid='$getuser' AND account='$account'");
			$sth->execute();
			$sth = $dbh->prepare("INSERT into transactioninfo ( date,time,userid,amount,account,prev_value,new_value,type,category,tags,ip,http_agent, comment ) VALUES ( CURDATE(), CURTIME(), '$getuser','$amount', '$account','$prev_amount', '$new_amount', '$ttype','$category','$tags','$ip','$info', '$comment')");
			$sth->execute();
			$sth->finish();
			$dbh->disconnect();
			$url = "view.cgi";
		} else {
			$url = "addtransaction.cgi";
		}
	} else {
		$url = "addtransaction.cgi";
	}
	
	my $t=1; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
}
1;