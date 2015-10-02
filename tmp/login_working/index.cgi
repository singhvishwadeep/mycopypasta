#!C:\Strawberry\perl\bin\perl.exe -w
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;

my $err = 0;

# look for cookies
my $session = cookie('cookie_id_mycopypasta');
print "Content-type: text/html\n\n";
if ($session ne "") {
	$session = new CGI::Session($session);
	print "Cookie found $session!\n";
	# check for session expiry
	if ( $session->is_expired ) {
		print "Session expired\n";
		#if session is expired then remove session and coookie
		require "removecookie.cgi";
	} else {
		print "Session is not expired\n";
		# if session is not expired
		if ($session->param('activelogin') eq "1") {
			# already logged in
			print "already logged in\n";
			my $url="welcome.html";
			my $t=1; # time until redirect activates
			print "<META HTTP-EQUIV=refresh CONTENT=\"$t;URL=$url\">\n";
			die;
		} elsif ($session->param('activelogin') eq "-1") {
			print "wrong password\n";
			# wrong password
			my $err = 1;
			$session->param('activelogin', "0");
		} else {
			print "something wrong relogin --$session->param('activelogin')--\n";
			# something wrong relogin
			require "removecookie.cgi";
		}
	}
} else {
	print "Cookie not found\n";
}
print "<html>\n";
print "<body>\n";
print "<a href = \"logout.cgi\">LOGOUT</a>";
print '<form method=POST action="validate.cgi">';
print 'Employee Name: <p><INPUT type="text" name="User" size=25 maxlength=25></p>';
print '<p>';
print 'Password:<p><INPUT TYPE=PASSWORD NAME="mypassword" id = "Password" size = "15" maxlength = "15" tabindex = "1"/></p>';
print '</p>';
print "<p><input type=\"submit\" value=\"Submit\" />--$err $rem--</p>";
if ($err) {
	print '<p>Wrong username/password</p>';
}
print '</form>';
print "</body> <\html> \n";

