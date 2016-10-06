import codecs, json, io
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter

XLSX_FILENAME='categories.xlsx'

class CacheData():
    def __init__(self, specs):
        self.specs = specs
        pass
    
    def generate(self):
        print("Start caching data...")
        
        fullpath = self.specs['input']['path'] + XLSX_FILENAME
        
        wb = load_workbook(fullpath)
        
        self.sheet =  wb.active
        row_count = self.sheet.max_row - 1
        max_column = self.sheet.max_column
        
        print('rows:' + str(row_count))
        print('columns:' + str(max_column) + ":" + get_column_letter(max_column))
        
        cahepath = self.specs['input']['path'] + XLSX_FILENAME + '.dump'
        
        print("opening cache file:" + cahepath)
        with io.open(cahepath, 'w', encoding='utf8') as f:
            range = 'A2:' + get_column_letter(max_column) + str(row_count)
            for row in self.sheet.iter_rows(range):
                row_dict = {}
                for cell in row:
                    self.store_cell(cell, row_dict)
                    
                str_row = json.dumps(row_dict, sort_keys=False, ensure_ascii=False).encode('utf8')

                f.write(unicode(str_row + '\n', 'utf8'))
                
    def store_cell(self, cell, dict):
        if (cell.value != None):
            if cell.column == 'A':
                dict['Cat0'] = cell.value
            elif cell.column == 'B':
                dict['Cat1'] = cell.value    
            elif cell.column == 'C':
                dict['Cat3'] = cell.value
            elif cell.column == 'D':
                dict['Cat4'] = cell.value
            elif cell.column == 'F':
                dict['id'] = int(cell.value)
            