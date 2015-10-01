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

my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
my $dbh = DBI->connect($dsn,"root","");
my $ip = $ENV{REMOTE_ADDR};
my $sth = $dbh->prepare("SELECT ip,date FROM iphold");
$sth->execute();
print "My IP -> <a href=\"http://www.ip-tracker.org/locator/ip-lookup.php?ip=$ip\" target=\"_blank\"> $ip </a> <br><br>";
$i = 0;
while (my $ref = $sth->fetchrow_hashref()) {
	my $currip = $ref->{'ip'};
	my $date = $ref->{'date'};
	print "$i) $date -> <a href=\"http://www.ip-tracker.org/locator/ip-lookup.php?ip=$currip\" target=\"_blank\"> $currip </a> <br>";		
	$i++;
}
$sth->finish();
$dbh->disconnect();
1;