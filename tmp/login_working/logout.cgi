#!C:\Strawberry\perl\bin\perl.exe -w

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;

# if cookie found then destroy the session
my $CGISESSID = cookie('cookie_id_mycopypasta');
if ($CGISESSID ne "") {
	my $session = CGI::Session->new($CGISESSID);
	$session->delete();
	$session->flush();
}

#destroying the cookie
my $cookie = cookie(-name=>'cookie_id_mycopypasta', -value=>"");
print header(-cookie=>$cookie);
print start_html("Removing MyCopyPasta Cookies");
print "<httpCookies httpOnlyCookies=\"true\" requireSSL=\"false\" />";
my $url="index.cgi";
my $t=1; # time until redirect activates
print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";