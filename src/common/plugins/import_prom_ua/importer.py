import io, json
import cache_groups
import cache_data
from common.image_loader import ImageURLLoader
from common.models.realm import Realm
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class Importer():
    def __init__(self, specs, filename, user, db):
        self.specs = specs
        self.user = user
        self.db = db
        self.filename = filename
    
#----------------------------------------------------------------------------------------------
    def run(self):
        
        print('start import items')
        
        cache = cache_data.CacheData(self.specs, self.filename, self.user, self.db)
        cache.cache()
        
        items = self.loadItems(cache.items_cache_filename)
        
        if len(items):
            print('start loading realm')
            self.realm = Realm(self.specs)
            self.realm.start()
        
            for item in items:
                self.storeItem(item)
                
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
        pass
#----------------------------------------------------------------------------------------------