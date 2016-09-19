from pymongo import MongoClient
from user_session_db import UserSessionDB

class LayoutDB:
	GROUPS_NAME = 'item_groups'
	ITEMS_NAME = 'items'

class ConnectionDB:
	def __init__(self, url):
		self.url = url
		self.connection = None
		self.db = None
		
	def connect(self):
		print('Connect to database...')
		self.connection = MongoClient(self.url)
		if not self.connection:
			raise Exception("Failed connect to database: %s", str(self.url))
		
		self.db = self.getDocument('shop7_test')
		if not self.db:
			raise Exception("Failed get document in database: %s", str(self.url))
		
		print self.db
		print('Connection OK')
		
	def close(self):
		self.connection.close()
		print('Connection closed')
		
	def getDocument(self, name):
		return self.connection[name]
	
	def getCollection(self, db, name):
		return db[name]
	
	def drop(self):
		if self.db:
			self.db[LayoutDB.GROUPS_NAME].drop()
			self.db[LayoutDB.ITEMS_NAME].drop()