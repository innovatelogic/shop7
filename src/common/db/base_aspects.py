from types.types import Category

BASE_ASPECTS = 'base_aspects'

class BaseAspects():
    def __init__(self, instance):
        self.instance = instance
        pass
    
    def init(self):
        self.cat = self.instance.connection.db[BASE_ASPECTS]
        
    def clear(self, aspect):
        self.cat.update_one({'_id':aspect}, {'$set': {"categories" : []}})
        
    def add_category(self, aspect, category):
        self.cat.update_one({'_id':aspect}, {'$push': {"categories" : category.get()}})
    
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()