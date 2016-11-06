from connection import ConnectionDB
from user_groups import UserGroups
from users import Users
from items import Items
from categories import Categories
from base_aspects import BaseAspects
from user_aspects import UserAspects

class Instance():
	''' incapsulate db management'''
	def __init__(self, specs):
		self.specs = specs
		self.connection = ConnectionDB(self.specs)
		self.user_groups = UserGroups(self)
		self.users = Users(self)
		self.items = Items(self)
		self.categories = Categories(self)
		self.base_aspects = BaseAspects(self)
		self.user_aspects = UserAspects(self)
		
	def connect(self):
		self.connection.connect()
		self.user_groups.init()
		self.users.init()
		self.items.init()
		self.categories.init()
		self.base_aspects.init()
		self.user_aspects.init()
		
	def disconnect(self):
		self.connection.close()
		pass
		