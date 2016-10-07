from common.connection_db import ConnectionDB, LayoutDB
from bson.objectid import ObjectId

class BuilderDB():
    def __init__(self, specs, tree):
        self.specs = specs
        self.tree = tree
        self.connection = None
        
    def connect(self):
        self.connection = ConnectionDB(self.specs)
        self.connection.connect()
        
    def close(self):
        self.connection.close()
            
    def build(self):
        '''write to db and generate mapping file'''
        self.connect()
        
        self.connection.db[LayoutDB.CATEGORIES].drop()
        
        categories_db = self.connection.getCollection(self.connection.db, LayoutDB.CATEGORIES)
        
        stack = []
        
        stack.append(self.tree.root)
        while len(stack):
            top = stack.pop(0)
            top.id = ObjectId()
            
            category_record = {'_id': top.id, 'parent_id': top.parent_id, 'name':top.name}
            categories_db.insert(category_record)
            
            for child in top.childs:
                child.parent_id = top.id
                stack.insert(0, child)
        
        self.close()
        pass
        