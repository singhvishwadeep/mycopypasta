#!C:\Strawberry\perl\bin\perl.exe -w

use DBI;
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;

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
	my $sth = $dbh->prepare("SELECT id,mysession,myip FROM userdatabase where myusername='$usr' AND mypassword='$pwd' AND activeaccount=1");
	$sth->execute();
	my $cookie_id = "";
	my $IP = "";
	my $err = 1;
	while (my $ref = $sth->fetchrow_hashref()) {
		$err = 0;
		$cookie_id = $ref->{'mysession'};
		$IP = $ref->{'myip'};
		$userid = $ref->{'id'};
#		print "Found a row: mysession = $ref->{'mysession'}, id = $ref->{'id'} -->$userid<--<br/>";
	}
	$sth->finish();
	$dbh->disconnect();
	
	if ($err) {
		#print "Wrong password<br/>";
		$url = "loginerrcookie.cgi";
	} else {
		$session->param('logged_in_user_mycp',$usr);
		$session->param('logged_in_userid_mycp',$userid);
		$url = "loginsetcookie.cgi?username=$usr";
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