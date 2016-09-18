import os, sys, shutil, argparse
import codecs, json, io
from openpyxl import load_workbook
import cache_items
import cache_groups
import builder_db
import cache_data

def main():

	reload(sys)
	
	sys.setdefaultencoding('utf8')

	parser = argparse.ArgumentParser()

	print("start script")
	
	cur_file_dir = os.path.dirname(os.path.realpath(__file__))
	proj_dir = os.path.dirname(cur_file_dir)
	
	print ('curr file dir:' + cur_file_dir)
	print ('proj dir:' + proj_dir)
	
	cache = cache_data.CacheData(cur_file_dir + '\..\data\\')
	cache.cache()

	#build database
	builder = builder_db.BuilderDB(cache.groups_cache_filename, cache.items_cache_filename)
	builder.build()
	
	return 1
	
if __name__== "__main__":
	main()