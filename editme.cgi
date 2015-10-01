#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;
use CGI::Session;
use DBI;
use DBD::mysql;
use POSIX 'strftime';

# new cgi query
my $q = new CGI;
# fetching cookie
my $ssid = $q->cookie('MYCOPYPASTACOOKIE');
# printing header
print $q->header;
# login error or not
my $err = 0;
# proper logged in?
my $login = 0;

if($ssid eq "") {
	# empty/no cookie found. Hence not logged in
} else {
	# cookie has some value, hence loading session from $ssid
	$session = CGI::Session->load($ssid) or die "$!";
	if($session->is_expired || $session->is_empty) {
		# if session is expired/empty, need to relogin
	} else {
		my $value = $session->param('logged_in_status_mycp');
		if ($value eq "1") {
			# properly logged in
			$login = 1;
		}
	}
}

if ($login == 0) {
	my $url="index.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
	die;
}


sub  trim { 
	my $s = shift;
	$s =~ s/^\s+|\s+$//g;
	return $s;
}

my $username=param('username');
my $id = param('id');
my $name=param('name');
my $email=param('email');
my $filename=param('file');
my $dob=param('dob');
my $identitylock=param('identitylock');
my $secquestion=param('secquestion');
my $secanswer=param('secanswer');
my $occupation=param('occupation');
my $place=param('place');

$username = trim($username);
$name = trim($name);
$id = trim($id);
$email = trim($email);
$filename = trim($filename);
$dob = trim($dob);
$identitylock = trim($identitylock);
$secquestion = trim($secquestion);
$secanswer = trim($secanswer);
$occupation = trim($occupation);
$place = trim($place);
	
if ($username ne "" && $id ne "" && $email ne "") {
	my $dsn = "DBI:mysql:database=mycopypasta;host=localhost";
	my $dbh = DBI->connect($dsn,"root","");
	
	$sth = $dbh->prepare("update userdatabase set mydob = '$dob',name = '$name',myemail='$email',myidentitylock='$identitylock',mysecurityquestion='$secquestion',mysecurityanswer='$secanswer',myprofession='$occupation',myplace='$place' where myusername='$username' AND id='$id'");
	$sth->execute();
	$sth->finish();
	
	if ($filename ne "") {
		my $userid = $id;
		my $Date = strftime '%Y-%m-%d', localtime;
		my $upload_dir = "images/$Date\_uploaded_files";
		mkdir "$upload_dir", 0777 unless -d "$upload_dir";
		$filename =~ s/.*[\/\\](.*)/$1/;
		$filename =~ s/ /_/g;
		my $upload_filehandle = $q->upload("file");
		my $directory_filename = "$upload_dir/$filename";
		# upload the file to the server
		open UPLOADFILE, ">$directory_filename";
		binmode UPLOADFILE;
		while ( <$upload_filehandle> )
		{
		    print UPLOADFILE;
		}
		close UPLOADFILE;
		# Open the file
		open MYFILE, $directory_filename || print "Cannot open file";
		my $blob_file;
		# Read in the contents
		while (<MYFILE>) {
		    $blob_file .= $_;
		}
		close MYFILE;
		$query = "update userdatabase set displaypic=? where id=?";
		$sth = $dbh->prepare($query);
		$sth->execute($blob_file,$userid) || print "Can't access database";
		$sth->finish;
		$dbh->disconnect();
		unlink $directory_filename;
	}
	my $url="profile.cgi?id=$id";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
} else {
	my $url="index.cgi";
	my $t=0; # time until redirect activates
	print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
}
	
1;