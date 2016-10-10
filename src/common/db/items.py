from types import Item

ITEMS_CATEGORY_NAME = 'items'

class Items():
    def __init__(self, connection):
        self.connection = connection
        
    def init(self):
        self.cat = self.connection.db[ITEMS_CATEGORY_NAME]
    
    def add_item(self, item):
        self.cat.insert(item.get())
    
    def remove_item(self, id):
        pass
    
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()
    