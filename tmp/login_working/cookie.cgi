#!C:\Strawberry\perl\bin\perl.exe -w

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;

$session = new CGI::Session();
$CGISESSID = $session->id();

my $cookie = cookie(-name=>'cookie_id_mycopypasta', -value=>$CGISESSID);
print header(-cookie=>$cookie);
print start_html("Cookie");
print "<httpCookies httpOnlyCookies=\"true\" requireSSL=\"false\" />";
print <<EndOfHTML;
<h2>Welcome $main::var!</h2>
Your cookie is $CGISESSID.<p>
EndOfHTML
print end_html;