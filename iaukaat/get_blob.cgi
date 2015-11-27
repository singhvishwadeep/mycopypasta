#!C:\Strawberry\perl\bin\perl.exe -w
use DBI;
use DBD::mysql;
use CGI;
$query = new CGI;
$profileid = $query->param("id");
my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
my $dbh = DBI->connect($dsn,"root","");
$query = "select id,displaypic from userdatabase where id = '$profileid'";
$sth = $dbh->prepare($query);
$sth->execute();
my $show = 0;
while (@data = $sth->fetchrow_array()) {
	$profileid = $data[0];
	$blob_file = $data[1];
	if ($blob_file ne "") {
		print "content-type: image/xyz\n\n";
		print $blob_file;
		$sth->finish;
		$show = 1;
	} else {
		$sth->finish;
		$query = "select defaultimage from default_attributes";
		$sth = $dbh->prepare($query);
		$sth->execute();
		while (@data = $sth->fetchrow_array()) {
			$blob_file = $data[0];
			if ($blob_file ne "") {
				print "content-type: image/xyz\n\n";
				print $blob_file;
				$sth->finish;
				$show = 1;
			}
			break;
		}
	}
	break;
}
if ($show == 0) {
	$sth->finish;
	$query = "select defaultimage from default_attributes";
	$sth = $dbh->prepare($query);
	$sth->execute();
	while (@data = $sth->fetchrow_array()) {
		$blob_file = $data[0];
		if ($blob_file ne "") {
			print "content-type: image/xyz\n\n";
			print $blob_file;
			$sth->finish;
			$show = 1;
		}
		break;
	}
}
$dbh->disconnect;