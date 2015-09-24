#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;

print header();
print start_html("Cookie");
print h2("Welcome!");

my $session = cookie('cookie_id_mycopypasta');
if ($session ne "") {
   print "Your cookie is $session.<br>";
} else {
   print "You don't have a cookie named `mycookie'.<br>";
}

print end_html;