#!/usr/bin/python
print "content-type:text/html\n"

import cgi
import cgitb
import random
from commands import getstatusoutput


getstatusoutput('rm -f /var/www/cgi-bin/cookies')
print '<script>alert("Loged out")</script>\n'
print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/login.html">\n'