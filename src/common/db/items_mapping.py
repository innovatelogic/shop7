from types.types import ItemMapping
from bson.objectid import ObjectId

ITEMS_MAPPING_NAME = 'items_mapping'

class ItemsMapping():
    def __init__(self, instance):
        self.instance = instance
        
    def init(self):
        self.cat = self.instance.connection.db[ITEMS_MAPPING_NAME]
    
    def add_mapping(self, mapping):
        self.cat.insert(mapping.get())
    
    def remove_mapping(self, id):
        ''' removes item from db. return boolean result '''
        out = False
        data = self.cat.find_one({'_id':id})
        if data:
            self.cat.remove({"_id": data['_id']})
            out = True
        return out
    
    def remove_mapping_id(self, item_id, mapping_id):
        pass
    
    def get_mapping(self, id):
        data = self.cat.find_one({'_id':id})
        if data:
            return ItemMapping(data)
        return None
    
    def update_mapping(self, item_id, mapping):
        pass
    
    def get_mappings_by_aspect_category(self, aspect, category_id):
        pipeline = [
                {'$unwind':'$mapping'},
                {'$match': {"mapping.{}".format(aspect):ObjectId(category_id)} },
                ]
            
        cursor = self.cat.aggregate(pipeline)
        return list(cursor)
            
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()