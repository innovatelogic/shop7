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
            
            new_stack = []
            for item in stack:
                item._id = ObjectId()
                
                category_record = {'_id': item._id, 'parent_id': item.parent_id, 'name':item.name}
                categories_db.insert(category_record)
            
                mapping[str(item._id)] = item.id
            
                for child in item.childs:
                    child.parent_id = item._id
                    new_stack.append(child)
            stack = new_stack
       
        self.save_mapping(mapping)
        self.close()
        pass
    
    def save_mapping(self, mapping):
        ''' save mapping from old id <-> new id'''
        fullpath = self.specs['input']['out'] + 'cat_mapping.map'
        print("opening damp categories mapping file:" + fullpath)
        with io.open(fullpath, 'w', encoding="utf8") as f:
            for key, value in mapping.iteritems():
                row = {'id_key':str(key), 'id_val':str(value)}
                str_json = json.dumps(row, sort_keys=False, ensure_ascii=False).encode('utf8')
                f.write(unicode(str_json + '\n', 'utf8'))
                
        