#!C:\Strawberry\perl\bin\perl.exe -w

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use DBI;
use CGI::Session;
print "Content-type: text/html\n\n";



if (param('User') and param('Password'))
{
	my $usr=param('User');
	my $pwd=param('mypassword');
	print "$usr $pwd --->\n";
	
}
