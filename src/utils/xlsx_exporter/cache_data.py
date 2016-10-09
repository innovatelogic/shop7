import codecs, json, io
import time
from openpyxl import load_workbook
import cache_items
import cache_groups

XLSX_FILENAME = 'data.xlsx'
CACHE_GROUPS_FILENAME = 'db_cache_groups.json'
CACHE_ITEMS_FILENAME = 'db_cache.json'

SHEET_GROUPS = 'Export Groups Sheet'
SHEET_ITEMS = 'Export Products Sheet'

class CacheData:
    def __init__(self, specs):
        self.specs = specs
        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.groups_cache_filename = self.specs['path']['data'] + 'cache_groups_' + self.specs['user']['login'] + '_' + timestr + '.json'
        self.items_cache_filename = self.specs['path']['data'] + 'cache_items_' + self.specs['user']['login'] + '_' + timestr + '.json'
        
    def cache(self):
        print('Start caching data..')
                
        wb = load_workbook(self.specs['path']['data'] + XLSX_FILENAME)

        print wb.get_sheet_names()
        
        groups_cache = cache_groups.CacheGroupsDB(self.groups_cache_filename, wb.get_sheet_by_name(SHEET_GROUPS))
        groups_cache.generate()
    
        items_cache = cache_items.CacheItemsDB(self.items_cache_filename, wb.get_sheet_by_name(SHEET_ITEMS))
        items_cache.generate()
        
        print 'cache OK'