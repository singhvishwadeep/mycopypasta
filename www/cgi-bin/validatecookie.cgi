#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;

print "Content-type: text/html\n\n";
my $err = 0;

# look for cookies
my $session = cookie('MYCOPYPASTACOOKIE');
if ($session ne "") {
	print "Cookie found $session valudatecookie!\n";
} else {
	print "Cookie not found valudatecookie\n";
}