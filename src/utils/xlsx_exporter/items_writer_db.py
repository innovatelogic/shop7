#from common.db.connection import LayoutDB
from group_tree import find_node_by_id
from bson.objectid import ObjectId
from common.db.types.types import Item

class ItemsWriterDB:
    def __init__(self, items, groups_root, db, user):
        self.items = items
        self.groups_root = groups_root
        self.db = db
        self.user = user
               
    def write(self):
        print ('Start write items to database...')
        
        for item in self.items:
            
            #self.id = spec['_id']
            #self.user_id = spec['user_id']
            #self.user_group_id = spec['user_group_id']
            #self.category = spec['category_id']
            #self.name = spec['name']
            #self.amount = spec['amount']
            #self.price = spec['price']
            #self.currency = spec['currency']
            #self.characteristics = []
            #FIELD_NAME = 'characteristicName'
            
            record = {'name':item['name']}
            
            record['_id'] = ObjectId()
            record['user_id'] = self.user._id
            record['user_group_id'] = self.user.group_id
            record['category_id'] = 0
            
            if 'keywords' in item:
                record['keywords'] = item['keywords']
                
            if 'desc' in item:
                record['desc'] = item['desc']
            
            if 'price' not in item:
                print('WARNING! item # %s have not price. Set \'0\'' % item['uniqID'])
                record['price'] = 0
            else:
                record['price'] = item['price']
            
            if 'currency' not in item:
                print('WARNING! item # %s have not currency. Set \'UAH\'' % item['uniqID'])
                record['currency'] = 'UAH'
            else:
                record['currency'] = item['currency']
                
            if 'unit' in item:
                record['unit'] = item['unit']
                
            if 'imageRefs' in item:
                record['imageRefs'] = item['imageRefs']
                
            if 'availability' in item:
                record['availability'] = item['availability']
            
            if 'amount' in item:
                record['amount'] = item['amount'] 
            else:
                print('WARNING! Item\'s # %s does not have amount. Set to default value 1' % item['uniqID'])
                record['amount'] = 1
                
            if 'groupID2' in item:
                group = find_node_by_id(item['groupID2'], self.groups_root)
                if group:
                    record['group_id'] = group._id
                else:
                    print('WARNING! Item\'s # %s group ID not found set Root' % item['uniqID'])
            else:
                print('WARNING! Item\'s # %s group ID not found set Root' % item['uniqID'])
                record['group_id'] = self.groups_root._id
                    
            for idx in range(0, Item.CHARACTERISTICS_MAX):
                field = 'characteristicName' + str(idx)
                if field in item:                 
                    record[field] = item[field]
            
            self.db.items.add_item(Item(record))
            
        print ('Write items OK')