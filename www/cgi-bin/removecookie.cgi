#!C:\Strawberry\perl\bin\perl.exe -w

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;

# if cookie found then destroy the session
#my $CGISESSID = cookie('MYCOPYPASTACOOKIE');
#if ($CGISESSID ne "") {
#	my $session = CGI::Session->new($CGISESSID);
#	$session->delete();
#	$session->flush();
#}
print "Content-type: text/html\n\n";
#destroying the cookie
my $cookiemy = cookie(-name=>'MYCOPYPASTACOOKIE', -value=>'',-expires => '-1d');


