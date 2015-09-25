#!C:\xampp\perl\bin\perl.exe

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI;
use CGI::Cookie qw();

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
	$usr=param('User');
	$pwd=param('mypassword');
	
	$dsn = "DBI:mysql:database=mycopypasta;host=localhost";
	$dbh = DBI->connect($dsn,root,"");
	my $sth = $dbh->prepare("SELECT cookie,IP FROM employee where emp_name='$usr' AND emp_password='$pwd'");
	$sth->execute();
	$err = 1;
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
		my $cookie = $query->cookie (-name=> 'MYCOPYPASTACOOKIE', -value   => '', -expires => '-1d');
		my $IP = $ENV{REMOTE_ADDR};
		my $cookie_id = "$usr.".random_id().".$IP";
		print "$cookie_id<br/>";
		my $sth = $dbh->prepare("UPDATE employee set `cookie`='$cookie_id',`IP`='$IP' where emp_name='$usr' AND emp_password='$pwd';");
		$sth->execute();
		$sth->finish();
		# creting a new cookie
		my $cookie = $query->cookie (-name=>'MYCOPYPASTACOOKIE', -value=> '$cookie_id');
		
		#check cookie exists or not!
		$theCookie = $query->cookie('MYCOPYPASTACOOKIE');
		print "theCookie = $theCookie<br/>";
		
		my %cookiesf = CGI::Cookie->fetch;
		print "theCookie = $cookiesf{'MYCOPYPASTACOOKIE'} <br/>";

		print ("Welcome $usr, you have entered correct password your cookie is $cookie_id<br />");
		
		my $cookie1 = CGI::Cookie->new(-name=>'V',-value=>$cookie_id);
		my $retrieve_cookie = cookie('V');
		print ("Cookie value is $retrieve_cookie<br />");


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