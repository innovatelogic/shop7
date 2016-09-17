import os, sys, shutil, argparse
import codecs, json, io
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
import cache_items
import cache_groups
import group_tree_generator

def main():

	reload(sys)
	
	sys.setdefaultencoding('utf8')

	parser = argparse.ArgumentParser()

	print("start script")
	
	cur_file_dir = os.path.dirname(os.path.realpath(__file__))
	proj_dir = os.path.dirname(cur_file_dir)
	data_dir = cur_file_dir + '\..\data\\'
	
	groups_cache_filename = data_dir + 'db_cache_groups.json'
	items_cache_filename = data_dir + 'db_cache.json'
	
	print ('cur_file_dir:' + cur_file_dir)
	print ('proj_dir:' + proj_dir)
	print ('data_dir:' + data_dir)
	
	wb = load_workbook(data_dir + 'data.xlsx')

	print wb.get_sheet_names()
	
	#generate cache
	groups_cache = cache_groups.CacheGroupsDB(groups_cache_filename, wb.get_sheet_by_name("Export Groups Sheet"))
	#groups_cache.generate()
	
	items_cache = cache_items.CacheItemsDB(items_cache_filename, wb.get_sheet_by_name("Export Products Sheet"))
	#items_cache.generate()

	#build data
	groups = group_tree_generator.GropTreeGenerator(groups_cache_filename)
	groups.generate()
	
	
	
	return 1
	
if __name__== "__main__":
	main()