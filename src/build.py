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
	parser.add_argument('-a', '--all', action='store_true', help='rebuild all data')
	parser.add_argument('-c', '--cache', action='store_true', help='rebuild all data')
	parser.add_argument('--out', type=str, help='data destination')
	parser.add_argument('--user', type=str, help='user')
	
	args = parser.parse_args()
	
	try:
		print("start script")
		
		cur_file_dir = os.path.dirname(os.path.realpath(__file__))
		proj_dir = os.path.dirname(cur_file_dir)
		
		print ('curr file dir:' + cur_file_dir)
		print ('proj dir:' + proj_dir)
		
		cache = cache_data.CacheData(cur_file_dir + '\..\data\\')
		
		build_cache = False

		if hasattr(args, 'a') or hasattr(args, 'all') or hasattr(args, 'c') or hasattr(args, 'cache'):
			build_cache = True
			
		if build_cache:	
			cache.cache()
	
		#build database
		builder = builder_db.BuilderDB(cache)
		builder.build()
		
	except Exception:
		print(sys.exc_info()[0])
		print(sys.exc_info()[1]) 
		
	return 1
	
if __name__== "__main__":
	main()