import os
import commands
import cgi, cgitb

cgitb.enable()

print "Content-Type: text/html\n"
form = cgi.FieldStorage()
filedata = form['upload']


if filedata.file: # field really is an upload
    with file("downloaded.txt", 'w') as outfile:
        outfile.write(filedata.file.read())
