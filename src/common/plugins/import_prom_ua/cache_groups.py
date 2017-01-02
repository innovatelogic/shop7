import os, sys, shutil, argparse
import codecs, json, io
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from common.db.types.types import Category
from common.aspect import Aspect, CategoryNode


#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class CacheGroupsDB:
	def __init__(self, sheet):
		self.sheet = sheet
		root_category = Category({'_id': -1, 'parent_id': None, 'name':'root'})
		root_category_node = CategoryNode(root_category, None)
		self.aspect = Aspect('', root_category_node)

#----------------------------------------------------------------------------------------------
	def generate(self):
		print("generate group cache...")
		
		row_count = self.sheet.max_row - 1
		max_column = self.sheet.max_column
		
		print('rows:' + str(row_count))
		print('columns:' + str(max_column) + ":" + get_column_letter(max_column))
		
		range = 'A3:' + get_column_letter(max_column) + str(row_count)
		for row in self.sheet.iter_rows(range):
			dict = {}
			for cell in row:
				self.store_cell(cell, dict)
			
			if dict['GroupNumber'] not in self.aspect.hashmap:
				
				parent_node = None
				if 'GroupParentNumber' in dict:
					if dict['GroupParentNumber'] not in self.aspect.hashmap:
						parent_node = self.loadById(dict['GroupParentNumber'])
					else:
						parent_node = self.aspect.hashmap[dict['GroupParentNumber']]
				else:
					parent_node = self.aspect.root

				new_node = CategoryNode(Category({'_id': dict['GroupNumber'], 'parent_id': None, 'name':dict['GroupName']}), parent_node)
				parent_node.childs.append(new_node)
				self.aspect.hashmap[str(dict['GroupNumber'])] = new_node

#----------------------------------------------------------------------------------------------
	def store_cell(self, cell, dict):
		if (cell.value != None):
			if cell.column == 'A':
				dict['GroupNumber'] = str(cell.value)
			elif cell.column == 'B':
				dict['GroupName'] = str(cell.value)
			#elif cell.column == 'C':
			#	dict['GroupID'] = cell.value
			elif cell.column == 'D' and cell.value:
				dict['GroupParentNumber'] = str(cell.value)
			#elif cell.column == 'E':
			#	dict['GroupParentID'] = cell.value
			
#----------------------------------------------------------------------------------------------		
	def loadById(self, str_id):
		parent_node = None
		print('red')
		row_count = self.sheet.max_row - 1
		max_column = self.sheet.max_column
		
		print('rows:' + str(row_count))
		print('columns:' + str(max_column) + ":" + get_column_letter(max_column))
		
		range = 'A3:' + get_column_letter(max_column) + str(row_count)
		for row in self.sheet.iter_rows(range):
			dict = {}
			for cell in row:
				self.store_cell(cell, dict)
				
			if dict['GroupNumber'] == str_id and dict['GroupNumber'] not in self.aspect.hashmap:
				if 'GroupParentNumber' in dict:
					if dict['GroupParentNumber'] not in self.aspect.hashmap:
						parent_node = self.loadById(dict['GroupParentNumber'])
					else:
						parent_node = self.aspect.hashmap[dict['GroupParentNumber']]
				else:
					parent_node = self.aspect.root

				new_node = CategoryNode(Category({'_id': dict['GroupNumber'], 'parent_id': None, 'name':dict['GroupName']}), parent_node)
				parent_node.childs.append(new_node)
				self.aspect.hashmap[str(dict['GroupNumber'])] = new_node
				
		print('green')
		return parent_node