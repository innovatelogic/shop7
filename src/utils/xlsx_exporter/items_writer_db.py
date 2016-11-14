import time, io, json
from group_tree import find_node_by_id
from bson.objectid import ObjectId
from common.db.types.types import Item, ItemMapping

from category_mapping import CategoryMapping

class ItemsWriterDB:
    def __init__(self, specs, items, realm, user):
        self.specs = specs
        self.items = items
        self.realm = realm
        self.user = user
        self.mapping = CategoryMapping(self.specs)
        self.mapping.init()
        self.image_map = {}

#----------------------------------------------------------------------------------------------               
    def write(self):
        print ('Start write items to database...')
        
        self.img_map = {}
        
        num = 0
        max_num = self.specs['opt']['nitem']
        
        for item in self.items:
            
            if (max_num > 0):
                if (num >= max_num):
                    break
                num += 1
            
            record = {'name':item['name'],
                      '_id':ObjectId(),
                      'user_id':self.user._id,
                      'user_group_id':self.user.group_id
                      }
            
            #if 'subsectionID' in item:
            #    subsection = item['subsectionID']
            #    category_id = self.mapping.get_category(str(subsection))
            #    if category_id:
            #        record['category_id'] = category_id
             #   else:
            #        print('WARNING! category # %s have not found in mapping. Set \'0\'' % subsection)
            #        record['category_id'] = 0
            #else:
            #    print('WARNING! item # %s have not category. Set \'0\'' % item['uniqID'])
            #    record['category_id'] = 0
            
            #if 'keywords' in item:
            #    record['keywords'] = item['keywords']
                
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
                self.img_map[record['_id']] = item['imageRefs']
                
            if 'availability' in item:
                record['availability'] = item['availability']
            
            if 'amount' in item:
                record['amount'] = item['amount'] 
            else:
                print('WARNING! Item\'s # %s does not have amount. Set to default value 1' % item['uniqID'])
                record['amount'] = 1

            for idx in range(0, Item.CHARACTERISTICS_MAX):
                field = 'characteristicName' + str(idx)
                if field in item:                 
                    record[field] = item[field]
            
            time_now = time.asctime()
            record['creation_time'] = time_now
            record['update_time'] = time_now
            record['mapping_id'] = ObjectId()
            
            mapping_spec = {'_id':record['mapping_id'],
                            'item_id':record['_id'],
                            'mapping':{}
                            }   


            self.realm.db.items.add_item(Item(record))

            if 'subsectionID' in item:
                subsection = item['subsectionID']
                category_id = self.mapping.get_category(str(subsection))
                
                node_category = self.realm.base_aspects_container.get_aspect_category('prom_ua', category_id)
                
                if node_category:
                    mapping_spec['mapping']['prom_ua'] = node_category.category._id
                else:
                    print('WARNING! category # %s have not found in mapping. Set \'0\'' % subsection)
            
            node_mapping = ItemMapping(mapping_spec)
            
            self.realm.db.items_mapping.add_mapping(node_mapping)
                
        print ('Write items OK')
        
#----------------------------------------------------------------------------------------------        
    def save_ref_mapping(self, filename):
        ''' save image mapping'''
        print("opening image mapping file:" + filename)
        with io.open(filename, 'w', encoding="utf8") as f:
            for key, value in self.img_map.iteritems():
                row = {'id':str(key), 'refs':str(value)}
                str_json = json.dumps(row, sort_keys=False, ensure_ascii=False).encode('utf8')
                f.write(unicode(str_json + '\n', 'utf8'))