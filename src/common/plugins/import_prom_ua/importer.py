import io, json, time
import cache_groups
import cache_data
from bson.objectid import ObjectId
from common.db.types.types import Category
from common.image_loader import ImageURLLoader
from common.models.realm import Realm
from common.db.types.types import Item, ItemMapping

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class Importer():
    def __init__(self, specs, filename, user, user_group, db, keep_groups = False):
        self.specs = specs
        self.user = user
        self.user_group = user_group
        self.user_aspect = db.user_aspects.get_aspect(user_group.aspect_id)
        self.db = db
        self.filename = filename
        self.realm = Realm(self.specs)
        self.keep_groups = keep_groups
        
#----------------------------------------------------------------------------------------------
    def run(self):
        
        print('start import items')
        
        cache = cache_data.CacheData(self.specs, self.filename, self.user, self.db)
        cache.cache()
        
        items = self.loadItems(cache.items_cache_filename)
        
        if len(items):
            print('start loading realm')
            
            self.realm.start()
            
            print('items processing...')
        
            n_count = 0

            for item in items:
                id = self.storeItem(item)
                if id:
                    n_count += 1
                    pass
            print('{}:items added, {}:skipped'.format(n_count, len(items) - n_count))
            self.realm.stop()
            
        else:
            print('no items cached')
            
        print('finish import items')

#----------------------------------------------------------------------------------------------
    def loadItems(self, filename):
        print ('opening items cache file:' + filename)
        items = []
        with io.open(filename, 'r', encoding = 'utf8') as f:
            print 'opening OK'
            for line in f:
                items.append(json.loads(line))
        return items

#----------------------------------------------------------------------------------------------
    def storeItem(self, item):
        record = {'name':item['name']}

        if 'desc' in item:
            record['desc'] = item['desc']
        
        if 'price' not in item:
            #print('WARNING! item # %s have not price. Set \'0\'' % item['uniqID'])
            record['price'] = 0
        else:
            record['price'] = item['price']
        
        if 'currency' not in item:
            #print('WARNING! item # %s have not currency. Set \'UAH\'' % item['uniqID'])
            record['currency'] = 'UAH'
        else:
            record['currency'] = item['currency']
            
        if 'unit' in item:
            record['unit'] = item['unit']
            
        if 'imageRefs' in item:
            record['imageRefs'] = item['imageRefs']
            #self.img_map[record['_id']] = item['imageRefs']
            
        if 'availability' in item:
            record['availability'] = item['availability']
        
        if 'amount' in item:
            record['amount'] = item['amount'] 
        else:
            #print('WARNING! Item\'s # %s does not have amount. Set to default value 1' % item['uniqID'])
            record['amount'] = 1

        for idx in range(0, Item.CHARACTERISTICS_MAX):
            field = 'characteristicName' + str(idx)
            if field in item:                 
                record[field] = item[field]
        
        
        # get user categry
        user_category_node = None
        if 'user_category' in item and self.keep_groups:
            user_category_node = self.EnsureUserCategory(self.user_aspect, item['user_category'])
        if not user_category_node:
            user_category_node = self.realm.user_aspects_container.get_aspect_default_category(self.user_aspect)
        
        # get prom_ua category
        prom_ua_category_node = None
        if 'subsectionID' in item:
            prom_ua_category_node = self.realm.getBaseAspectCategoryByForeignId('prom_ua', item['subsectionID'])
        else:
            prom_ua_category_node = self.realm.getBaseAspectDefaultCategory('prom_ua')
        
        if not prom_ua_category_node:
            return None
        
        return self.realm.addItem(self.user._id,
                record,
                user_category_node.category._id,
                'prom_ua',
                prom_ua_category_node.category._id)

#----------------------------------------------------------------------------------------------
    def EnsureUserCategory(self, user_aspect, category_path):
        ''' check category_path parameter and create if it's not exist.
        otherwise return default category
        @param aspect [in] user aspect object 
        @param category_path [in] slash splitted path
        @return categoryNode
        '''
        
        category_path = category_path.replace('root/', '')
        category_words = category_path.split('/')
        user_category_node = user_aspect.node_root
        
        bFail = False
        
        for name in category_words:
            node = user_category_node.getChildByName(name)
    
            if node:
                user_category_node = node
                continue
            else:
                parent_id = user_category_node.category._id
                
                new_category = Category({'_id': ObjectId(), 'parent_id': parent_id, 'name':name})
                
                self.db.user_aspects.add_category(user_aspect._id, new_category)
                self.user_aspect.addChildCategory(user_category_node, new_category) 
                
                user_category_node = user_category_node.getChildByName(name)
            
        return user_category_node