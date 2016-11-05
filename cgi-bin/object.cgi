#!/usr/bin/python
import cgi,cgitb
from commands import getstatusoutput
import random
import socket
from time import sleep
cgitb.enable()

print "content-type: text/html"
print ""

block=cgi.FormContent()
#user=block['user'][0]
size=block['size'][0]

def auth():
	cookies = getstatusoutput('sudo cat cookies')
	if cookies[0] == 0 :
		user_name = cookies[1].split(':')[0]
		password = cookies[1].split(':')[1]
		lvcreate(user_name)
	else :
		print '<script>alert("Log in First")</script>\n'
		print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/login.html">\n'




def lvcreate(user):
	a = str(random.randint(1,5000))
	l = 'sudo lvcreate -V{1}G --name {0}{2} --thin cloud/cloud'.format(user,size,a)
	crt = getstatusoutput(l)
	chk = 0
	if crt[0] == 0 :
		getstatusoutput('sudo mkfs.ext4 /dev/cloud/{0}{1}'.format(user,a))
		getstatusoutput('sudo mkdir /{0}{1}'.format(user,a))
		getstatusoutput('sudo mount /dev/cloud/{0}{1} /{0}{1}'.format(user,a))
		s = socket.socket()
		s.connect(('192.168.122.81',11111))
		s.send(user)
		sleep(1)
		s.send(size)
		sleep(1)
		s.send(a)
		s.close()
		chk = 1
		gluster(user,a,chk)
	else :
		print 'error'


def gluster(user,a,chk) :
	if chk == 1:
		gvc = getstatusoutput('sudo gluster volume create {0}{1} 192.168.1.100:/{0}{1} 192.168.122.81:/{0}{1} force'.format(user,a))
		print gvc
		gvs = getstatusoutput('sudo gluster volume start {0}{1}'.format(user,a))
		#print gvs
		make_tar(user,a)
	else :
		print '<script>alert("storage not ready")</script>\n'
		print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/stass_login.html">\n'



def make_tar(user,a):
	b = str(random.randint(1000, 9999))
	sh_write = "sudo echo -e 'mkdir /media/{0}{1} \n mount 192.168.1.100:/{0}{1} /media/{0}{1}\n'  >> {0}{2}.sh".format(user,a,b)
	sh = getstatusoutput(sh_write)
	print sh
	getstatusoutput('sudo mkdir /var/www/html/down/{0}'.format(user))
	getstatusoutput('sudo chmod +x  {0}{1}.sh'.format(user,b))
	getstatusoutput('sudo tar -cvf  {0}{1}.tar {0}{1}.sh'.format(user,b))
	getstatusoutput('sudo mv {0}{1}.tar /var/www/html/down/{0}/'.format(user,b))
	print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/down/{0}/{0}{1}.tar">\n'.format(user,b)


auth()
