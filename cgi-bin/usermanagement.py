#!/usr/bin/python
print "content-type:text/html\n"
import cgi
import cgitb
import pymongo
from commands import getstatusoutput

login = cgi.FormContent()
userid = login['username'][0]
password = login['password'][0]
try :
	new = login['new'][0]
except:
	new = None
client = pymongo.MongoClient()
database = client['test']
db = database.test 



def new_user() :
	print 'new user'
	try :
		ifl = db.insert_one({"userid":userid,"password":password})
		
		print '<script>alert("Account created. Now login to continue.")</script>\n'
		print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/login.html">\n'
		
	except:
		print '<script>alert("username already exists")</script>\n'
		print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/login.html">\n'
		print 'username already in use' 
	


def user_login():
	try :
		print 'in try'
		cursor = db.find({"userid":userid,"password":password})
		print cursor
		case = None
		for log in cursor:
			case = log
		if case != None :
			getstatusoutput('echo {0}:{1} > cookies'.format(userid,password))
			print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/index.html">\n'
		else :
			print '<script>alert("invalid username or password")</script>\n'
			print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/login.html">\n'
			
	except:
		print '<script>alert("invalid username or passsword")</script>\n'
		print '<META HTTP-EQUIV=refresh CONTENT="0;URL=http://192.168.1.100/login.html">\n'



def check():
	if new == 'checked' :
		print 'in if'
		new_user()
	else :
		print 'in else'
		user_login()


check()
    