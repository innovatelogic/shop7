import codecs, json, io, time
from openpyxl import load_workbook
import cache_items
import cache_groups

SHEET_GROUPS = 'Export Groups Sheet'
SHEET_ITEMS = 'Export Products Sheet'

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class CacheData:
    def __init__(self, specs, filename, user, db):
        self.specs = specs
        self.db = db
        self.filename = filename
        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.groups_cache_filename = self.specs['path']['data'] + 'cache_groups_' + user.name + '_' + timestr + '.json'
        self.items_cache_filename = self.specs['path']['data'] + 'cache_items_' + user.name + '_' + timestr + '.json'
        
        print(self.items_cache_filename)
        print(self.groups_cache_filename)

#----------------------------------------------------------------------------------------------
    def cache(self):
        file_path = self.specs['path']['data'] + self.filename
        
        print('Start caching data {}'.format(file_path))
                
        wb = load_workbook(file_path)
        
        groups_cache = cache_groups.CacheGroupsDB(wb.get_sheet_by_name(SHEET_GROUPS))
        groups_cache.generate()
        
        items_cache = cache_items.CacheItemsDB(self.specs, self.items_cache_filename, wb.get_sheet_by_name(SHEET_ITEMS))
        items_cache.generate(groups_cache.aspect)
        
        print 'cache OK'