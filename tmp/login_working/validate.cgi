#!C:\Strawberry\perl\bin\perl.exe -w

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use DBI;
use CGI::Session;
print "Content-type: text/html\n\n";

require "cookie.cgi";
my $CGISESSID = cookie('cookie_id_mycopypasta');
my $session = CGI::Session->new($CGISESSID);

if (param('User') and param('mypassword'))
{
	my $usr=param('User');
	my $pwd=param('mypassword');
	
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
		$session->param(activelogin => "-1");
	} else {
		$session->param(activelogin => "1" );
	}
} else {
	$session->param(activelogin => "-1");
}

my $url="index.cgi";
my $t=1; # time until redirect activates
print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";