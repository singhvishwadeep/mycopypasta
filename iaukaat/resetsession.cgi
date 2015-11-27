#!C:\Strawberry\perl\bin\perl.exe

use CGI;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Session ('MYCOPYPASTASESSION');

$session = CGI::Session->load() or die CGI::Session->errstr;
$session->delete();
$session->flush(); 

1;