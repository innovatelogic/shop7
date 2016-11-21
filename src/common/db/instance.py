from connection import ConnectionDB
from user_groups import UserGroups
from users import Users
from items import Items
from categories import Categories
from base_aspects import BaseAspects
from user_aspects import UserAspects
from items_mapping import ItemsMapping
from user_settings import UserSettingsDB

class Instance():
	''' incapsulate db management'''
	def __init__(self, specs):
		self.specs = specs
		self.connection = ConnectionDB(self.specs)
		self.user_groups = UserGroups(self)
		self.users = Users(self)
		self.user_settings = UserSettingsDB(self)
		self.items = Items(self)
		self.categories = Categories(self)
		self.base_aspects = BaseAspects(self)
		self.user_aspects = UserAspects(self)
		self.items_mapping = ItemsMapping(self)
		
	def connect(self):
		self.connection.connect()
		self.user_groups.init()
		self.users.init()
		self.user_settings.init()
		self.items.init()
		self.categories.init()
		self.base_aspects.init()
		self.user_aspects.init()
		self.items_mapping.init()
		
	def disconnect(self):
		self.connection.close()
		pass
		