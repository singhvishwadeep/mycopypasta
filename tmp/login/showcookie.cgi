#!C:\Strawberry\perl\bin\perl.exe -wT
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;

print header();
print start_html("Cookie");
print h2("Welcome!");

if (my $cookie = cookie('mycookie')) {
   print "Your cookie is $cookie.<br>";
} else {
   print "You don't have a cookie named `mycookie'.<br>";
}

print end_html;
