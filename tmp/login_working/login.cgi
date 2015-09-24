#!C:\Strawberry\perl\bin\perl.exe -w

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use warnings;
use diagnostics;

my $query = new CGI;
use DBI;

sub random_id {
    my $rid = "";
    my $alphas = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    my @alphary = split(//, $alphas);
    foreach my $i (1..32) {
       my $letter = $alphary[int(rand(@alphary))];
       $rid .= $letter;
    }
    return $rid;
}

print "Content-type: text/html\n\n";

if (param('User') and param('mypassword'))
{
	my $usr=param('User');
	my $pwd=param('mypassword');
	
	my $dsn = "DBI:mysql:database=userpass;host=localhost";
	my $dbh = DBI->connect($dsn,"root","");
	my $sth = $dbh->prepare("SELECT cookie,IP FROM employee where emp_name='$usr' AND emp_password='$pwd'");
	$sth->execute();
	my $err = 1;
	my $cookie_id = "";
	my $IP = "";
	while (my $ref = $sth->fetchrow_hashref()) {
		$err = 0;
		if ($ref->{'cookie'} ne "") {
			$cookie_id = $ref->{'cookie'};
			$IP = $ref->{'IP'};
		}
		#print "Found a row: id = $ref->{'emp_id'}, name = $ref->{'emp_name'}<br/>";
	}
	$sth->finish();
	if ($err) {
		$dbh->disconnect();
		print ("You entered the wrong username/password.<br />");
		die;
	} else {
		# deleting any previous cookie
		#my $cookie = $query->cookie (-name=> 'cookie_id_mycopypasta', -value   => '', -expires => '-1d');
		my $cookie = cookie(-name=>"cookie_id_mycopypasta", -value=>"", -expires => '-1d');
		my $IP = $ENV{REMOTE_ADDR};
		#my $cookie_id = "$usr.".random_id().".$IP";
		my $cookie_id = int(rand(1000000));
		print "$cookie_id<br/>";
		my $sth = $dbh->prepare("UPDATE employee set `cookie`='$cookie_id',`IP`='$IP' where emp_name='$usr' AND emp_password='$pwd';");
		$sth->execute();
		$sth->finish();
		# creting a new cookie
		#my $cookie = $query->cookie (-name=>'cookie_id_mycopypasta', -value=> '$cookie_id');
		my $cookie = cookie(-name=>"cookie_id_mycopypasta", -value=>$cookie_id);
		#check cookie exists or not!
		if (my $cookie = cookie('cookie_id_mycopypasta')) {
		   print "Your cookie is $cookie.<br>";
		} else {
		   print "You don't have a cookie named `mycookie'.<br>";
		}


		$dbh->disconnect();
	}	
	
	#print start_html("Environment");
	#foreach my $key (sort(keys(%ENV))) {
		#print "$key = $ENV{$key}<br>\n";
	#}
	#print end_html;
}



print "<html>\n";
print "<body>\n";






print '</form>';
print "</body><\html>\n";