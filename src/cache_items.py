import os, sys, shutil, argparse
import codecs, json, io
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter

class CacheItemsDB:
	def __init__(self, filename, sheet):
		self.filename = filename
		self.sheet = sheet
		
	def generate(self):
		print("generate...")
		
		row_count = self.sheet.max_row - 1
		max_column = self.sheet.max_column
		
		print('rows:' + str(row_count))
		print('columns:' + str(max_column) + ":" + get_column_letter(max_column))
		
		print("opening cache file")
		with io.open(self.filename, 'w', encoding='utf8') as f:
			range = 'B1:' + get_column_letter(max_column) + str(row_count)
			for row in self.sheet.iter_rows(range):
				row_dict = {}
				for cell in row:
					self.store_cell(cell, row_dict)
			
				json_str = json.dumps(row_dict, ensure_ascii=False)
				#json.dump(row_dict, f)
				f.write(json_str + '\n')
				
	def store_cell(self, cell, dict):
		if (cell.value != None):
			if cell.column == 'B':
				dict['Name'] = cell.value
			elif cell.column == 'C':
				dict['Keywords'] = cell.value
			elif cell.column == 'D':
				dict['Desc'] = cell.value
			elif cell.column == 'E':
				dict['Type'] = cell.value
			elif cell.column == 'F':
				dict['Price'] = cell.value
			elif cell.column == 'G':
				dict['Currency'] = cell.value
			