import cache_groups
import cache_data

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
        
        print('finish import items')
        
        pass