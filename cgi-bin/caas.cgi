#!/usr/bin/python
print "content-type:text/html\n"

import cgi
import cgitb
import random
from commands import getstatusoutput


caas = cgi.FormContent()
cgitb.enable()
#user = caas['user'][0]
container = caas['container'][0]
cnt = caas['no_of_containers'][0]
no_of_containers = int(cnt)

def auth():
    cookies = getstatusoutput('sudo cat cookies')
    if cookies[0] == 0 :
        user = cookies[1].split(':')[0]
        password = cookies[1].split(':')[1]
        create_containers(user)
    else :
        print '<script>alert("Log in First")</script>\n'
        print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/login.html">\n'


def create_containers(user) :
    f=('{}.html'.format(user))
    print f
    h=open(f,'a+')
    for i in range(no_of_containers) :
        port = str(random.randint(10000,20000))
	cr = getstatusoutput('sudo docker run -itd --name {0}{1}{2} -p {2}:4200  caas'.format(user,str(i),port))
	ip = getstatusoutput("sudo docker exec  {0}{1}{2} hostname -i".format(user,str(i),port))[1]
        h.write('<a href="http://192.168.1.100:{1}" target="_blank">{0}</a><br />\n'.format(ip,port))
	getstatusoutput('sudo mkdir /var/www/html/containers/{0}'.format(user))
	getstatusoutput('sudo mv {0}.html /var/www/html/containers/{0}/'.format(user))
	
    h.close()
    print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://172.17.0.1/containers/{0}/{0}.html">\n'.format(user)

auth()

#-v /root/Documents/rhel7:/yum1 -v /root/Documents/rhel7rpm/:/yum2