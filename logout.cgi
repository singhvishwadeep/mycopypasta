#!C:\Strawberry\perl\bin\perl.exe

use DBI;
use CGI;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
my $q = new CGI;
# Create new cookies and send them
$cookie1 = CGI::Cookie->new(-name=>'MYCOPYPASTACOOKIE',-value=>'',-expires=>now);
$cookie2 = CGI::Cookie->new(-name=>'MYCOPYPASTACOOKIEUSER',-value=>'',-expires=>now);
print $q->header(-cookie=>[$cookie1,$cookie2]);
my $url="index.cgi";
my $t=0; # time until redirect activates
print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
1;