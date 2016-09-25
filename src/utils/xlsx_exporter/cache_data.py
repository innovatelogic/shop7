import codecs, json, io
from openpyxl import load_workbook
import cache_items
import cache_groups

XLSX_FILENAME = 'data.xlsx'
CACHE_GROUPS_FILENAME = 'db_cache_groups.json'
CACHE_ITEMS_FILENAME = 'db_cache.json'

SHEET_GROUPS = 'Export Groups Sheet'
SHEET_ITEMS = 'Export Products Sheet'

class CacheData:
    def __init__(self, path):
        self.path = path
        self.groups_cache_filename = self.path + CACHE_GROUPS_FILENAME
        self.items_cache_filename = self.path + CACHE_ITEMS_FILENAME
        
    def cache(self):
        print 'Start caching data..'
                
        wb = load_workbook(self.path + XLSX_FILENAME)

        print wb.get_sheet_names()
        
        groups_cache = cache_groups.CacheGroupsDB(self.groups_cache_filename, wb.get_sheet_by_name(SHEET_GROUPS))
        groups_cache.generate()
    
        items_cache = cache_items.CacheItemsDB(self.items_cache_filename, wb.get_sheet_by_name(SHEET_ITEMS))
        items_cache.generate()
        
        print 'cache OK'