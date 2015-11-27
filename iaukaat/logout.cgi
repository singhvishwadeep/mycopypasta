#!C:\Strawberry\perl\bin\perl.exe

use DBI;
use CGI;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use DBI;

# new cgi query
my $q = new CGI;
# fetching cookie
my $ssid = $q->cookie('MYCOPYPASTACOOKIE');
$session = CGI::Session->load($ssid) or die "$!";

if($session->is_expired || $session->is_empty) {
	# if session is expired/empty, need to relogin
} else {
	my $value = $session->param('logged_in_status_mycp');
	if ($value eq "1") {
		my $getuser = $session->param('logged_in_userid_mycp');
		my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
		my $dbh = DBI->connect($dsn,"root","");
		$sth = $dbh->prepare("update userdatabase set loggedin='0' where id='$getuser'");
		$sth->execute();
		$sth->finish();
		$dbh->disconnect();
	}
}


$session->delete();
$session->flush();
# Create new cookies and send them
$cookie1 = CGI::Cookie->new(-name=>'MYCOPYPASTACOOKIE',-value=>'',-expires=>now);
print $q->header(-cookie=>[$cookie1]);
my $url="index.cgi";
my $t=0; # time until redirect activates
print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
1;