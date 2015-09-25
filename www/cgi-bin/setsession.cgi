
#!C:\Strawberry\perl\bin\perl.exe

use CGI;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Session ('MYCOPYPASTASESSION');

$session = new CGI::Session();
$session->expire('+1h');    # expire after 1 hour
print $session->header();
$session->flush();

1;