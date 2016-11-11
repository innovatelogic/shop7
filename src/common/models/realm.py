import common.db.instance
from category_model import CategoryModel
from users_model import UsersModel
from items_cache_model import ItemsCacheModel
from base_aspects_container import BaseAspectsContainer
from user_aspects_container import UserAspectsContainer

class Realm():
    def __init__(self, specs):
        self.specs = specs
        self.db = common.db.instance.Instance(self.specs)
        self.category_model = CategoryModel(self.db)
        self.users_model = UsersModel(self.db)
        self.items_cache_model = ItemsCacheModel(self.db)
        self.base_aspects_container = BaseAspectsContainer(self.db)
        self.user_aspects_container = UserAspectsContainer(self.db)
        pass
    
    def start(self):
        self.db.connect()
        self.base_aspects_container.load()
        
    def stop(self):
        self.db.disconnect()