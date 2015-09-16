#!C:/xampp/perl/bin/perl.exe
use DBI;
use CGI qw/:standard/;

print "Content-type: text/html\n\n";
print "<html><h1>OTT Login</h1></html>\n";

print '<form method=POST action="">';

print '<p>';
print 'Employee Name: <p><INPUT type="text" name="User" size=25 maxlength=25></p>';
print '</p>';
print '<p>';
print 'Password:<p><INPUT TYPE=PASSWORD NAME="mypassword" id = "Password" size = "15" maxlength = "15" tabindex = "1"/></p>';
print '</p>';
print '<p><input type="submit" value="Submit" /></p>';
print '</form>';
if (param('User') and param('mypassword')) {
	$usr=ucfirst(lc(param('User')));
	$pwd=ucfirst(lc(param('mypassword')));
	
	my $driver = "mysql";
	my $database = "mycopypasta";
	my $user = "root"; 
	my $password = "";
	my $dbh = DBI->connect("DBI:$driver:$database",$user, $password,) or die "$DBI::errstr\n";
	$sth=$dbh->prepare("Select emp_id from employee where emp_name='$usr'") || die "$DBI::errstr\n";
	$sth->execute() || die "$DBI::errstr\n";	
	$sth1 = $dbh->prepare("Select emp_password from employee where emp_password='$pwd'") or &dbdie;
	$sth1->execute() || die "$DBI::errstr\n";
	if ($x=$sth->fetchrow()) {
		if ($y=$sth1->fetchrow()) {
	         print "Correct Password, Welcome";
		} else {
			print "Incorrect Password";
		}
	} else {
		print "Incorrect Emp_Id";
	}
	$dbh->disconnect || die "$DBI::errstr\n";
}