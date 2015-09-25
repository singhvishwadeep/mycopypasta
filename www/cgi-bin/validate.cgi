#!C:\Strawberry\perl\bin\perl.exe -w

use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use DBI;
use CGI::Session ('MYCOPYPASTASESSION');
$q = new CGI;
print $q->header(-cache_control=>"no-cache, no-store, must-revalidate");
$session = new CGI::Session();
$session->expire('+1h');    # expire after 1 hour
print $session->header(-location=>'validate.cgi');

#require "setsession.cgi";
#my $session = CGI::Session->load() or die CGI::Session->errstr;

if (param('User') and param('Password'))
{
	my $usr=param('User');
	my $pwd=param('Password');
	
	my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
	my $dbh = DBI->connect($dsn,"root","");
	my $sth = $dbh->prepare("SELECT cookie,IP FROM employee where emp_name='$usr' AND emp_password='$pwd'");
	$sth->execute();
	my $err = 1;
	my $cookie_id = "";
	my $IP = "";
	while (my $ref = $sth->fetchrow_hashref()) {
		$err = 0;
		if ($ref->{'cookie'} ne "") {
			$cookie_id = $ref->{'cookie'};
			$IP = $ref->{'IP'};
		}
		#print "Found a row: id = $ref->{'emp_id'}, name = $ref->{'emp_name'}<br/>";
	}
	$sth->finish();
	$dbh->disconnect();
	
	if ($err) {
		print "Wrong password<br/>";
		$session->param('activelogin', '0');
	} else {
		print "Correct password<br/>";
		$session->param('activelogin', '1');
	}
} else {
	print "Dont know password<br/>";
	$session->param('activelogin', '0');
}

my $var = $session->param('activelogin');

if($session->is_expired) {
	print "Session is_expired\n";
} elsif($session->is_empty) {
	print "Session is_empty\n";
} else {
	print "Session is present --$var---\n";
	if ($var eq "1") {
		print "already logged in\n";
	} else {
		print "wrong password\n";
	}
}

print "GET ME -$session- ->$var<-<br/>";

my $url="../../index.cgi";
my $t=1; # time until redirect activates
#print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
1;