from openpyxl import load_workbook

XLSX_FILENAME="categories.xlsx"

class CacheData():
    def __init__(self, path):
        self.path = path
        pass
    
    def generate(self):
        print("Start caching data")
    
        wb = load_workbook(self.path + XLSX_FILENAME)
    