#!C:\Strawberry\perl\bin\perl.exe -w

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;

print "Content-type: text/html\n\n";
$session = new CGI::Session();
$CGISESSID = $session->id();
my $cookiemy = cookie(-name=>'MYCOPYPASTACOOKIE', -value=>$CGISESSID,-expires => '+7d');

