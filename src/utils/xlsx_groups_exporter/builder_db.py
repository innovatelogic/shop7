import codecs, json, io
from common.db.connection import ConnectionDB, LayoutDB
from common.db.instance import Instance
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
        
        mapping = dict()
        stack = []
        
        stack.append(self.tree.root)
        while len(stack):
            top = stack.pop(0)
            
            top._id = ObjectId()
            mapping[str(top._id)] = top.id
            
            category_record = {'_id': top._id, 'parent_id': top.parent_id, 'name':top.name}
            categories_db.insert(category_record)
            
            for child in top.childs:
                child.parent_id = top._id
                stack.insert(0, child)
        
        self.save_mapping(mapping)
        self.close()
        pass
    
    def save_mapping(self, mapping):
        ''' save mapping from old id <-> new id'''
        fullpath = self.specs['input']['out'] + 'cat_mapping.map'
        print("opening damp categories mapping file:" + fullpath)
        with io.open(fullpath, 'w') as f:
            for key, value in mapping.iteritems():
                row = {'id_key':key, 'id_val':value}
                str_row = json.dumps(row, sort_keys=False, ensure_ascii=False)
                f.write(str_row.encode('ascii', 'ignore'))
                
        