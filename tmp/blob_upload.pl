#!C:\Strawberry\perl\bin\perl.exe -w
# DBI is the standard database interface for Perl
# DBD is the Perl module that we use to connect to the MySQL database
use DBI;
use DBD::mysql;
# use CGI for forms
use CGI;
use POSIX 'strftime'; # Need to explicitly load the functions in POSIX
# Note that if you pass no argument to localtime, it assumes the current time
$Date = strftime '%Y-%m-%d', localtime;
$database = "mycopypasta";
$upload_dir = "$Date\_uploaded_files";
#make directory unless it already exists
mkdir "$upload_dir", 0777 unless -d "$upload_dir";
$query = new CGI;
$filename = $query->param("file");
$serial_number = $query->param("serial_number");
print $query->header ( );
$filename =~ s/.*[\/\\](.*)/$1/;
$filename =~ s/ /_/g;
$upload_filehandle = $query->upload("file");
$directory_filename = "$upload_dir/$filename";
print "$filename $serial_number<br>";
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

#----------------------------------------------------------------------
# insert the values into the database
#----------------------------------------------------------------------
# invoke the ConnectToMySQL sub-routine to make the database connection
    $dbh = ConnectToMySql($database);
    # set the value of your SQL query
    $query = "insert into blobs (serial_number, blob_file) values (?, ?) ";
    $sth = $dbh->prepare($query);
	print $query;
    $sth->execute($serial_number, $blob_file) || print "Can't access database";
    $sth->finish;
    $dbh->disconnect;
	print "$filename $serial_number";
#----------------------------------------------------------------------
print " <TITLE>File Uploaded</TITLE>";
print " <font face=verdana size=2 color=#003366>Thanks for uploading your file!<br>";
print " <font face=verdana size=2 color=#003366>File directory: $Date\_uploaded_files<br>";
print " <font face=verdana size=2 color=#003366>Your file: $filename<br>";
print " <font face=verdana size=2 color=#003366>Your serial number: $serial_number<br>";
#----------------------------------------------------------------------
sub ConnectToMySql {
#----------------------------------------------------------------------
my ($db) = @_;
my $host="localhost";

    my $database = "mycopypasta";
    my $host = "localhost";
    my $userid = "root";
    my $passwd = "";
    # the chomp() function will remove any newline character from the end of a string
    chomp ($database, $host, $userid, $passwd);
my $connectionInfo="dbi:mysql:$database;$host";
# make connection to database
my $l_dbh = DBI->connect($connectionInfo,$userid,$passwd);
return $l_dbh;
}