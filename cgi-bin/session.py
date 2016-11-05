#!/usr/bin/python
print "content-type:text/html\n"
from os import environ
import cgi,cgitb
cgitb.enable()


for param in environ.keys():
  print param
  print environ[param]

if "HTTP_COOKIE" in environ:
    print environ["HTTP_COOKIE"]
else:
    print "HTTP_COOKIE not set!"
'''

if environ.has_key('HTTP_COOKIE'):
	for cookie in map(strip,split(environ['HTTP_COOKIE'],';')):
		(key,value) = split(cookie,'=')
		if key == "UserId":
			user_id = value
		if key == "Password":
			password = value

print user_id
print password
'''