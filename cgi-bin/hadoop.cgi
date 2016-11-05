#!/usr/bin/python
import cgi,cgitb
from commands import getstatusoutput
import random
import socket
from time import sleep
cgitb.enable()

print "content-type: text/html"
print ""

hadoop = cgi.FormContent()
no_of_datanodes = int(hadoop['datanodes'][0])

def auth():
	cookies = getstatusoutput('sudo cat cookies')
	if cookies[0] == 0 :
		user_name = cookies[1].split(':')[0]
		password = cookies[1].split(':')[1]
		namenode(user_name)
	else :
		print '<script>alert("Log in First")</script>\n'
		print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/login.html">\n'

def namenode(user):
	port = str(random.randint(10000,20000))
	nn = getstatusoutput('sudo docker run -itd --name nn{0}{1} -p {1}:4200  namenode'.format(user,port))
	namenode_ip = getstatusoutput("sudo docker exec  {0}{1} hostname -i".format(user,port))[1]
	datanodes_cluster(user)
	sleep(1)
	datanode_conf_ansible(namenode_ip,user)
	laun(namenode_ip)


def datanodes_cluster(user):
	h=open('datanodes','a+')
	for i in range(no_of_datanodes) :
        	port = str(random.randint(20000,30000))
		dn = getstatusoutput('sudo docker run -itd --name dn{0}{1}{2} -p {2}:4200  datanode'.format(user,str(i),port))
		datanode_ip = getstatusoutput("sudo docker exec  dn{0}{1}{2} hostname -i".format(user,str(i),port))[1]
        	h.write('{}     ansible_ssh_user=root ansible_ssh_pass=q\n'.format(datanode_ip,port))
		getstatusoutput('sudo mkdir /var/www/html/containers/{0}'.format(user))
		getstatusoutput('sudo mv datanodes /var/www/html/containers/{0}/'.format(user))
	
def datanode_conf_ansible(namenode_ip,user):
	nmr = getstatusoutput("sudo ansible all -i /var/www/html/containers/{0}/datanodes -m lineinfile -a \"dest=/etc/hadoop/core-site.xml regexp='<value>hdfs://namenode:10001</value>' line='<value>hdfs://172.17.0.2:10001</value>'\"".format(user))
	mpr = getstatusoutput("sudo ansible all -i /var/www/html/containers/{0}/datanodes -m lineinfile -a \"dest=/etc/hadoop/mapred-site.xml regexp='<value>jobtracker:9002</value>' line='<value>172.17.0.2:9002</value>'\"".format(user))
	dns = getstatusoutput("sudo ansible all -i /var/www/html/containers/{0}/datanodes -m command -a 'hadoop-daemon.sh start datanode'".format(user))
	tts = getstatusoutput("sudo ansible all -i /var/www/html/containers/{0}/datanodes -m command -a 'hadoop-daemon.sh start tasktracker'".format(user))
	jps = getstatusoutput("sudo ansible all -i /var/www/html/containers/{0}/datanodes -m command -a '/usr/java/jdk1.7.0_79/bin/jps'".format(user))



def laun(namenode_ip):
	print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://{}:50070">\n'.format(namenode_ip)

auth()
