from connection import ConnectionDB
from user_groups import UserGroups
from users import Users
from items import Items

class Instance():
	''' incapsulate db management'''
	def __init__(self, specs):
		self.specs = specs
		self.connection = ConnectionDB(self.specs)
		self.user_groups = UserGroups(self)
		self.users = Users(self)
		self.items = Items(self)
		
	def connect(self):
		self.connection.connect()
		self.user_groups.init()
		self.users.init()
		self.items.init()
		
	def disconnect(self):
		self.connection.close()
		pass
		