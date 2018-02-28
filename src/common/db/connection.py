from pymongo import MongoClient
from common.utils import log
#from user_session_db import UserSessionDB

class LayoutDB:
	CATEGORIES = 'categories'
	GROUPS_NAME = 'item_groups'
	ITEMS_NAME = 'items'

#----------------------------------------------------------------------------------------------
class ConnectionDB:
	def __init__(self, specs):
		self.specs = specs
		self.connection = None
		self.db = None

#----------------------------------------------------------------------------------------------
	def connect(self):
		url = self.specs['db']['host'] + ':' + self.specs['db']['port'] + '/'
		
		log.Msg("Connect to database: " + url)
		
		self.connection = MongoClient(url)
		if not self.connection:
			raise Exception("Failed connect to database: %s" % url)
		
		self.db = self.getDocument(self.specs['db']['name'])
		if not self.db:
			raise Exception("Failed get document in database: %s" % url)
		
		log.MsgOk('Connection OK')

#----------------------------------------------------------------------------------------------
	def close(self):
		self.connection.close()
		log.Msg('Connection to database closed')

#----------------------------------------------------------------------------------------------
	def getDocument(self, name):
		return self.connection[name]

#----------------------------------------------------------------------------------------------
	def getCollection(self, db, name):
		return db[name]