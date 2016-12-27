from types.types import Category

CATEGORIES_NAME = 'categories'

#----------------------------------------------------------------------------------------------
class Categories():
    def __init__(self, instance):
        self.instance = instance

#----------------------------------------------------------------------------------------------
    def init(self):
        self.cat = self.instance.connection.db[CATEGORIES_NAME]

#----------------------------------------------------------------------------------------------
    def get_root_category(self):
        data = self.cat.find_one({'name':'root'})
        if data:
            return Category(data)
        return None

#----------------------------------------------------------------------------------------------
    def get_childs(self, parent):
        out = []
        if parent:
            records = self.cat.find({'parent_id':parent._id})
            for record in records:
                out.append(Category(record))
        return out
    
    #----------------------------------------------------------------------------------------------
    def drop(self):
        '''drop collection. rem in production'''
        #self.cat.drop()
        pass