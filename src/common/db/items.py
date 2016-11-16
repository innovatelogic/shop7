import time
from types.types import Item

ITEMS_CATEGORY_NAME = 'items'

class Items():
    def __init__(self, instance):
        self.instance = instance
        
    def init(self):
        self.cat = self.instance.connection.db[ITEMS_CATEGORY_NAME]
    
    def add_item(self, item):
        self.cat.insert(item.get())
    
    def remove_item(self, id):
        ''' removes item from db. return boolean result '''
        out = False
        data = self.cat.find_one({'_id':id})
        if data:
            self.cat.remove({"_id": data['_id']})
            out = True
        return out
    
    def get_item(self, id):
        data = self.cat.find_one({'_id':id})
        if data:
            return Item(data)
        return None
    
    def update_item(self, spec):
        pass
    
    def get_user_items(self, token, category_id, offset):
        data = self.cat.find({'category_id':category_id})
        items = []
        for i in data:
            items.append(Item(i))
        return items
    
    def get_all_items(self):
        '''retrieve all items from db'''
        out = []
        data = self.cat.find({})
        for item in data:
            out.append(Item(item))
        return out
    
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()
    