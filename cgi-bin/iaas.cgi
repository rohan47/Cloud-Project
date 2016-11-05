#!/usr/bin/python 
print "content-type:text/html\n"
import pymongo
from commands import getstatusoutput
from os import system
import cgi,cgitb
import random
import time

cgitb.enable()

login = cgi.FormContent()

#user_name = login['username'][0]
#password = login['password'][0]
ram_size = login['ram'][0]
hdd = login['sizeofhdd'][0]
cpu = login['cpucore'][0]
os_name = login['osname'][0]
os_inst = login['os'][0]



'''
def auth():

	f = open("users.txt",'r')
	users = f.readlines()
	f.close()

	for user in users:

		chk = user.split(':')

		if chk[0] == user_name :

			stp = password.strip()
			stpi = chk[1].strip()

			if stpi == stp :

				
				ram = ram_size
				hard_disk = hdd
				os = os_inst
				cpu_cores = cpu
				un = False
				install(ram, hard_disk, os, cpu_cores)

			else : 

				un = True

		else:
				un = True

	if un :
		print 'invalid username or password'
'''

def auth():
	cookies = getstatusoutput('sudo cat cookies')
	
	if cookies[0] == 0 :
		user_name = cookies[1].split(':')[0]
		password = cookies[1].split(':')[1]
		ram = ram_size
		hard_disk = hdd
		os = os_inst
		cpu_cores = cpu
		
		install(user_name, password, ram, hard_disk, os, cpu_cores)	##########--function_call#####
		database(user_name, password, ram, hard_disk, os, cpu_cores)
	else :
		print '<script>alert("Log in First")</script>\n'
		print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/login.html">\n'







def install(user_name,password,ram, hard_disk, os, cpu_cores) :

	instance = user_name + str(random.randint(1, 100))
	mk = getstatusoutput('sudo mkdir /var/lib/libvirt/images/{}'.format(user_name))
	print mk

	
	
	port = str(random.randint(5900, 5999))

	clone(user_name, instance, ram, hard_disk, os, cpu_cores, port)    ##########--function_call#####

	if os_name == 'windows8' :
		inst = getstatusoutput('sudo virt-install --import --hvm --name {0} --ram {1} --vcpu {2} --disk path=/var/lib/libvirt/images/winclone.qcow2 --graphics vnc,listen=0.0.0.0,port={4} --noautoconsole --force'.format(instance,ram,cpu_cores,user_name,port))
	#else :
	#	inst = getstatusoutput('sudo virt-install --import --hvm --name {0} --ram {1} --vcpu {2} --disk path=/var/lib/libvirt/images/{3}/{0}.qcow2 --graphics vnc,listen=0.0.0.0,port={4} --noautoconsole --force'.format(instance,ram,cpu_cores,user_name,port))
	
	#if inst[0] == 0 :

	vnc_connection(port,instance)    ##########--function_call#####
		
	#else :
	#	print inst






def clone(user_name, instance, ram, hard_disk, os, cpu_cores, port) :

	if os_name == 'redhat' :
		inst = getstatusoutput('sudo virt-install --import --hvm --name {0} --ram {1} --vcpu {2} --disk path=/var/lib/libvirt/images/rhel7.1-2neutron.qcow2 --graphics vnc,listen=0.0.0.0,port={4} --noautoconsole --force'.format(instance,ram,cpu_cores,user_name,port))
		#inst = getstatusoutput('sudo virt-clone --original rhel7.1-2neutron --name {0}del --file /var/lib/libvirt/images/{1}/{0}.qcow2'.format(instance,user_name))
		if inst[0] == 0 :
			print '<script>alert("Launching {}")</script>\n'.format(os_name)
		else :
			print inst

	elif os_name == 'windows8' :
		#inst = getstatusoutput('sudo virt-clone --original win8.1 --name {0}del --file /var/lib/libvirt/images/{1}/{0}.qcow2'.format(instance,user_name))
		inst = (0,1)
		if inst[0] == 0 :
			print '<script>alert("Launching {}")</script>\n'.format(os_name)
		else :
			print inst

	elif os_name == 'ubuntu' :
		inst = getstatusoutput('sudo virt-install --import --hvm --name {0} --ram {1} --vcpu {2} --disk path=/var/lib/libvirt/images/Ubuntu.qcow2 --graphics vnc,listen=0.0.0.0,port={4} --noautoconsole --force'.format(instance,ram,cpu_cores,user_name,port))
		#inst = getstatusoutput('sudo virt-clone --original Ubuntu --name {0}del --file /var/lib/libvirt/images/{1}/{0}.qcow2'.format(instance,user_name))
		if inst[0] == 0 :
			print '<script>alert("Launching {}")</script>\n'.format(os_name)
		else :
			print inst

	elif os_name == 'mint' :
		inst = getstatusoutput('sudo virt-install --import --hvm --name {0} --ram {1} --vcpu {2} --disk path=/var/lib/libvirt/images/Mint.qcow2 --graphics vnc,listen=0.0.0.0,port={4} --noautoconsole --force'.format(instance,ram,cpu_cores,user_name,port))
		#inst = getstatusoutput('sudo virt-clone --original Mint --name {0}del --file /var/lib/libvirt/images/{1}/{0}.qcow2'.format(instance,user_name))
		if inst[0] == 0 :
			print '<script>alert("Launching {}")</script>\n'.format(os_name)
		else :
			print inst
	
	elif os_name == 'kali' :
		inst = getstatusoutput('sudo virt-install --import --hvm --name {0} --ram {1} --vcpu {2} --disk path=/var/lib/libvirt/images/kali.qcow2 --graphics vnc,listen=0.0.0.0,port={4} --noautoconsole --force'.format(instance,ram,cpu_cores,user_name,port))
		#inst = getstatusoutput('sudo virt-clone --original kali --name {0}del --file /var/lib/libvirt/images/{1}/{0}.qcow2'.format(instance,user_name))
		if inst[0] == 0 :
			print '<script>alert("Launching {}")</script>\n'.format(os_name)
		else :
			print inst
	
	else :
		print '<script>alert("Internal Server Error")</script>\n'






'''
def install(user_name,password,ram, hard_disk, os, cpu_cores):
	
	print 'in install'
	no_error = True
	while no_error :
		print 'in while'
		getstatusoutput('sudo mkdir /var/lib/libvirt/images/'.format(user_name))
		qemui = 'sudo qemu-img create -f qcow2 /var/lib/libvirt/images/'+ user_name + '/' + os_name + '.qcow2 ' + hard_disk + 'G' 
		
		qemu_image = getstatusoutput(qemui)
		print qemu_image

		if qemu_image[0] == 0 :
			
			port = str(random.randint(5900, 5999))
			virt = 'virt-install --hvm --name ' + os_name + ' --memory ' + ram + ' --vcpu ' + cpu_cores + ' --location http://192.168.1.100/rhel/ --disk /var/lib/libvirt/images/'+ user_name + '/'  + os_name +'.qcow2 --graphics vnc,listen=0.0.0.0,port=' + port + ' --noautoconsole' 
			print port
			
			inst = getstatusoutput('sudo  ' + virt)
			print inst
 			if inst[0] == 0:

				print """

				<b> Os install Successful </b>
				<b> connect to 192.168.1.100:""" + port + """ </b>


				"""
				
				no_error = False
				vnc_connection(port)
'''







def vnc_connection(port,instance):
	print 'in vnc connect'
	random_port = str(random.randint(6000, 60000))
	print random_port
	sockify = 'sudo /var/www/cgi-bin/websockify-master/run -D 192.168.1.100:{0} 192.168.1.100:{1}'.format(random_port,port) #./run 192.168.2.162:5555{port of webserver} 192.168.2.162:5911{port of os}
	print sockify
	so = getstatusoutput(sockify)
	print so
	if so[0] == 0:
		getstatusoutput('qrencode -s 10x10 -o /var/www/html/qr/{0}.png http://192.168.1.100/vnc/index.html?ip=192.168.1.100\\&port={1}'.format(instance,random_port))
		
		h=open('/var/www/html/qr/{0}.html'.format(instance),'a+')
		h.write('<a href="http://192.168.1.100/vnc/index.html?ip=192.168.1.100&port='+random_port+'" target="_blank"><img src="http://192.168.1.100/qr/'+instance+'.png" width="200" height="200"></a>')
		h.close()
		print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/qr/{0}.html">\n'.format(instance)
		#print '<script>alert("Scan qr to view in phone")</script>\n'
		#print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/vnc/index.html?ip=192.168.1.100&port='+random_port+'">\n'
		
		#print '<META HTTP-EQUIV=refresh content="5; URL=javascript:window.open(\'http://192.168.1.100/qr{0}.png\',\'_parent\');">\n'.format(instance)
	else :
		print 'error'
	

def database(user_name, password, ram, hard_disk, os, cpu_cores):
	client = pymongo.MongoClient()
	database = client[user_name]
	db = database.test 
	ifl = db.insert_one({"username":user_name,"password":password,"instance_details":{"ram":ram,"hard_disk":hard_disk,"os":os,"cpu_cores":cpu_cores}})




auth()














 

#--extra-args='ip=...,subnet=... ,gateway=... ' 




















