from connection import ConnectionDB
from users import Users

class Instance():
	''' incapsulate db management'''
	def __init__(self, specs):
		self.specs = specs
		self.connection = ConnectionDB(self.specs)
		self.users = Users(self.connection)
		
	def connect(self):
		self.connection.connect()
		self.users.init()
		
	def disconnect(self):
		self.connection.close()
		pass
		