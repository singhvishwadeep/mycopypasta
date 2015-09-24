#!C:\xampp\perl\bin\perl.exe

print "Content-type: text/html\n\n";
print "<html>\n";
print "<body>\n";
print '<form method=POST action="login.cgi">';
print 'Employee Name: <p><INPUT type="text" name="User" size=25 maxlength=25></p>';
print '<p>';
print 'Password:<p><INPUT TYPE=PASSWORD NAME="mypassword" id = "Password" size = "15" maxlength = "15" tabindex = "1"/></p>';
print '</p>';
print '<p><input type="submit" value="Submit" /></p>';
print '</form>';
print "</body><\html>\n";






