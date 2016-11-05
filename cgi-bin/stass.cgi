#!/usr/bin/python
import cgi
from commands import getstatusoutput
import random

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
	l='sudo lvcreate -V{1}G --name {0}{2} --thin cloud/cloud'.format(user,size,a)
	crt=getstatusoutput(l)
	print crt #############################################################
	if crt[0] == 0 :
		print 'lv created'
		iscsi(user,a)
	else :
		print 'no success'


def iscsi(user,a):
	
	file = "sudo echo -e '<target {0}{1}>\n     backing-store  /dev/cloud/{0}{1}\n</target>' >> /etc/tgt/conf.d/{0}{1}.conf".format(user,a)
	tg=getstatusoutput(file)
	print tg
	getstatusoutput('sudo systemctl restart tgtd')
	if tg[0] == 0 :
		print 'storage ready'
		make_tar(user,a)
	else :
		print '<script>alert("storage not ready")</script>\n'
		print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/stass_login.html">\n'

def make_tar(user,a):
	
	sh_write = "sudo echo -e 'iscsiadm --mode discoverydb --type sendtargets --portal 192.168.1.100 --discover\niscsiadm --mode node --targetname {0}{1} --portal 192.168.1.100:3260 --login' >> {0}{1}.sh".format(user,a)
	sh = getstatusoutput(sh_write)
	print sh
	getstatusoutput('sudo mkdir /var/www/html/down/{0}'.format(user))
	getstatusoutput('sudo chmod +x  {0}{1}.sh'.format(user,a))
	getstatusoutput('sudo tar -cvf  {0}{1}.tar {0}{1}.sh'.format(user,a))
	getstatusoutput('sudo mv {0}{1}.tar /var/www/html/down/{0}/'.format(user,a))
	print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/down/{0}/{0}{1}.tar">\n'.format(user,a)


auth()


#iscsiadm --mode discoverydb --type sendtargets --portal 192.168.1.100 --discover\n