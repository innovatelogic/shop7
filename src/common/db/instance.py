from connection import ConnectionDB
from users import Users
from items import Items

class Instance():
	''' incapsulate db management'''
	def __init__(self, specs):
		self.specs = specs
		self.connection = ConnectionDB(self.specs)
		self.users = Users(self.connection)
		self.items = Items(self.connection)
		
	def connect(self):
		self.connection.connect()
		self.users.init()
		self.items.init()
		
	def disconnect(self):
		self.connection.close()
		pass
		