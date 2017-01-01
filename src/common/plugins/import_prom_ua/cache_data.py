import codecs, json, io, time
from openpyxl import load_workbook
import cache_items

SHEET_GROUPS = 'Export Groups Sheet'
SHEET_ITEMS = 'Export Products Sheet'

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class CacheData:
    def __init__(self, specs):
        self.specs = specs
        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        #self.groups_cache_filename = self.specs['path']['out'] + 'cache_groups_' + self.specs['user']['login'] + '_' + timestr + '.json'
        self.items_cache_filename = self.specs['path']['out'] + 'cache_items_' + self.specs['user']['login'] + '_' + timestr + '.json'

#----------------------------------------------------------------------------------------------
    def cache(self):
        
        filename = self.specs['path']['data'] + self.specs['path']['filename']
        
        print('Start caching data {}'.format(filename))
                
        wb = load_workbook(filename)

        #print wb.get_sheet_names()
        
        #groups_cache = cache_groups.CacheGroupsDB(self.groups_cache_filename, wb.get_sheet_by_name(SHEET_GROUPS))
        #groups_cache.generate()
    
        items_cache = cache_items.CacheItemsDB(self.specs, self.items_cache_filename, wb.get_sheet_by_name(SHEET_ITEMS))
        items_cache.generate()
        
        print 'cache OK'