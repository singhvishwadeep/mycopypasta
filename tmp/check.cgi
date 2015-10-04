#!C:\Strawberry\perl\bin\perl.exe -w
use strict;
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

print header;
print start_html("Environment");

foreach my $key (sort(keys(%ENV))) {
  print "$key = $ENV{$key}<br>\n";
}
print "HTTP_REFERER = $ENV{'HTTP_REFERER'}<br>\n";

print end_html;
#HTTP_USER_AGENT
#REMOTE_ADDR
#HTTP_REFERER