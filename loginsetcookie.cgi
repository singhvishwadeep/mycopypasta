#!C:\Strawberry\perl\bin\perl.exe

use DBI;
use CGI;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
my $q = new CGI;
# SETTING LOGIN COOKIES
$cookie1 = CGI::Cookie->new(-name=>'MYCOPYPASTACOOKIE',-value=>'1',expires=>'+7d');
$usr = $q->param('username');
$cookie2 = CGI::Cookie->new(-name=>'MYCOPYPASTACOOKIEUSER',-value=>$usr,expires=>'+7d');
print $q->header(-cookie=>[$cookie1,$cookie2,$cookie3]);
my $url="index.cgi";
my $t=0; # time until redirect activates
print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
1;