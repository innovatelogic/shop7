import codecs, json, io
from bson.objectid import ObjectId
import common.db.instance
from common.db.types.types import Category

class BuilderDB():
    def __init__(self, specs, tree):
        self.specs = specs
        self.tree = tree
        self.connection = None
        
    def connect(self):
        self.db = common.db.instance.Instance(self.specs)
        self.db.connect()

    def close(self):
        self.db.disconnect()
            
    def build(self):
        '''write to db and generate mapping file'''
        self.connect()
        
        #categories_db.insert({'_id':"prom_ua"})
        #categories_db.insert({'_id':"amazon"})
        #categories_db.insert({'_id':"ebay"})
        
        self.db.base_aspects.clear('prom_ua')
            
        mapping = dict()
        stack = []
        
        stack.append(self.tree.root)

        while len(stack):      
            new_stack = []
            for item in stack:
                item._id = ObjectId()
                
                cat = Category({'_id': item._id, 'parent_id': item.parent_id, 'name':item.name})
                self.db.base_aspects.add_category('prom_ua', cat)
                
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
                
        