#!C:\Strawberry\perl\bin\perl.exe -w

use DBI;
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use Digest::MD5 qw(md5 md5_hex md5_base64);

my $q = new CGI;

my $login = 0;

# creating a session
$session = new CGI::Session(); #initiate a session.
$id =$session->id();
$session->param('logged_in_status_mycp','0');
$session->expire('+1y');
# Create new cookies and send them
$cookie1 = CGI::Cookie->new(-name=>'MYCOPYPASTACOOKIE',-value=>$id);
print $q->header(-cookie=>[$cookie1]);
my $url="index.cgi";
my $userid = "";

if (param('User') and param('Password'))
{
	my $usr=param('User');
	my $pwd=param('Password');
	
	my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
	my $dbh = DBI->connect($dsn,"root","");
	my $sth = $dbh->prepare("SELECT id,mysession,myip,deleted,activeaccount,mypassword FROM userdatabase where myusername='$usr'");
	$sth->execute();
	my $userid = "";
	my $cookie_id = "";
	my $IP = "";
	my $err = 1;
	my $activeaccount = "";
	my $deleted = "";
	my $wrong = 1;
	while (my $ref = $sth->fetchrow_hashref()) {
		if ($ref->{'mypassword'} eq $pwd) {
			$cookie_id = $ref->{'mysession'};
			$IP = $ref->{'myip'};
			$userid = $ref->{'id'};
			$err = 0;
			$deleted = $ref->{'deleted'};
			$activeaccount = $ref->{'activeaccount'};
			$wrong = 0;
		}
		break;
#		print "Found a row: mysession = $ref->{'mysession'}, id = $ref->{'id'} -->$userid<--<br/>";
	}
	$sth->finish();
	
	if ($err == 0) {
		my $sth = $dbh->prepare("update userdatabase set mysession='$id',myip='$ENV{REMOTE_ADDR}' where id='$userid'");
		$sth->execute();
		$sth->finish();
	} else {
		my $sth = $dbh->prepare("update userdatabase set mysession='',myip='$ENV{REMOTE_ADDR}' where id='$userid'");
		$sth->execute();
		$sth->finish();
	}
	
	$dbh->disconnect();
	
	if ($wrong == 1) {
		#msg = 0; account deleted
		#msg = 1; account is not activated
		#msg = 2; wrong username/password
		my $msg = md5_hex('2');
		$url = "loginerrcookie.cgi?msg=$msg";
	} elsif ($deleted == 1) {
		my $msg = md5_hex('0');
		$url = "loginerrcookie.cgi?msg=$msg";
	} elsif ($activeaccount == 0) {
		my $msg = md5_hex('1');
		$url = "loginerrcookie.cgi?msg=$msg";
	} else {
		my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
		my $dbh = DBI->connect($dsn,"root","");
		my $ip = $ENV{REMOTE_ADDR};
		my $info = $ENV{HTTP_USER_AGENT};
		$sth = $dbh->prepare("INSERT into login_ip_track ( userid,username,ip,http_agent,date ) VALUES ( '$userid','$usr', '$ip','$info',NOW())");
		$sth->execute();
		$sth->finish();
		$dbh->disconnect();
		$session->param('logged_in_user_mycp',$usr);
		$session->param('logged_in_userid_mycp',$userid);
		$url = "loginsetcookie.cgi";
#		print "Correct password -$userid-<br/>";
		$login = 1;
	}
} else {
	$url="index.cgi";
	#print "Dont know password<br/>";
}

#print "Calling $url <br>";

my $t=1; # time until redirect activates
print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
1;