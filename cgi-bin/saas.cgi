#!/usr/bin/python2
print "content-type:text/html\n"

from commands import getstatusoutput
from os import system
import cgi,cgitb
import random
cgitb.enable()
login = cgi.FormContent()

username = login['username'][0]
password = login['password'][0]
try :
	soft = login['g'][0]
except:
	print '<script>alert("select a software")</script>\n'
	print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/saas_login.html">\n'


def useradd():
	 
	try : 
		us = getstatusoutput('sudo useradd -s /usr/bin/{1} {0}'.format(username,soft))
		ps = getstatusoutput('echo {0} |sudo  passwd {1} --stdin'.format(password,username))
		if us[0] == 0 and ps[0] == 0 :
			print 'save and run the file'
			make_tar()
		else :
			print '<script>alert("username already exists")</script>\n'
			
			print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/saas_login.html">\n'
	except : 
		#print '<script>alert("username already exists")</script>\n'
		print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/saas_login.html">\n'
	
	 
	

def make_tar():
	a = str(random.randint(1000, 9999))
	sh_write = "sudo echo -e 'ssh -X {0}@192.168.1.100' >> {0}{1}.sh".format(username,a)
	sh = getstatusoutput(sh_write)
	print sh
	
	
	getstatusoutput('sudo chmod +x  {0}{1}.sh'.format(username,a))
	getstatusoutput('sudo tar -cvf  {0}{1}.tar {0}{1}.sh'.format(username,a))
	getstatusoutput('sudo mv {0}{1}.tar /var/www/html/down/'.format(username,a))
	print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/down/{0}{1}.tar">\n'.format(username,a)
	

useradd()