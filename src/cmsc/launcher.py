import os, sys, shutil, argparse
import codecs, json, io
from openpyxl import load_workbook
from bson.objectid import ObjectId
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import common.db.instance
import common.connection_db
from common.models.base_aspects_container import BaseAspectsContainer, CategoryNode, BaseAspectHelper
from common.db.types.types import Category

#----------------------------------------------------------------------------------------------
class Opt():
	''' options incapsulator opt input {'str(option)': (str(desc), func, params), ... } '''
	def __init__(self, opt):
		self.opt = opt
		
	def optPrint(self):
		print('>>')
		for key, value in self.opt.iteritems():
			print('{} - {}'.format(key, value[0]))
		print('q - quit')
		
	def run(self):
		while(True):
			self.optPrint()
			flag = False
			line = raw_input().strip().lower()
			for key, value in self.opt.iteritems():
				if line == key:
					if value[1]:
						if value[1](value[2]) == 1: 
							return
					else:
						print('invalid operation')
					flag = True
					
			if line == 'q':
				break
			
			if not flag:
				print('invalid input')
				
#----------------------------------------------------------------------------------------------			
def createNewUserWithGroup(params):
	print('Create New user With New group')
	spec = {}
	
	print('enter user email (login)')
	spec['email'] = raw_input().strip().lower()
	
	print('enter user name')
	spec['name'] = raw_input().strip().lower()
	
	print('enter password')
	spec['pwhsh'] = raw_input().strip().lower()
	
	print('enter user phone')
	spec['phone'] = raw_input().strip().lower()
	
	params.users.addUser(spec, None, 'all')
	
	return 1

#----------------------------------------------------------------------------------------------
def createNewUserWithinExistedGroup(params):
	print('Create New user within existed group')
	return 1

#----------------------------------------------------------------------------------------------
def operateUserManagement(params):
	opt = Opt({'1':('create New user with New group', createNewUserWithGroup, (params)),
			   '2':('create New user within existed group', createNewUserWithinExistedGroup, (params))})
	opt.run()
	return 0
	
#----------------------------------------------------------------------------------------------
def operateDB(params):
	print('operate DB')
	print params
	db = common.db.instance.Instance(params)
	db.connect()
	
	print('red')
	opt = Opt({'1':('users management', operateUserManagement, db), 
			   '2':('categories management', None)})
	opt.run()

#----------------------------------------------------------------------------------------------
def main():
	reload(sys)
	
	sys.setdefaultencoding('utf8')

	parser = argparse.ArgumentParser()
	parser.add_argument('--dbhost', type=str, help='database host name')
	parser.add_argument('--dbport', type=str, help='database port')
	parser.add_argument('--dbname', type=str, help='database name')
	
	args = parser.parse_args()

	specs = {}
	specs['db'] = {
        'host':args.dbhost,
        'port':args.dbport,
        'name':args.dbname,
        }
	
	try:
		print("cmsc starting ...")
		
		opt = Opt({'1':('operate db', operateDB, specs), '2':('connect to MS', None)})
		opt.run()
		
		print("end script")
		
	except Exception:
		print(sys.exc_info()[0])
		print(sys.exc_info()[1]) 
		
	return 0
	
if __name__== "__main__":
	main()