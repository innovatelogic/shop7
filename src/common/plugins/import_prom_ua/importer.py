import cache_groups
import cache_data

class Importer():
    def __init__(self, specs, db, filename):
        self.specs = specs
        self.db = db
        self.filename = filename
        
    def import_(self):
        
        cache = cache_data.CacheData(self.specs)
        cache.cache()
        
        pass