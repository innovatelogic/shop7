import os, sys, shutil, argparse
import codecs, json, io
from openpyxl import load_workbook

from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

import cache_items
import cache_groups
import builder_db
import cache_data

def main():
	reload(sys)
	
	sys.setdefaultencoding('utf8')

	parser = argparse.ArgumentParser()
	
	parser.add_argument('--all', action='store_true', help='rebuild all data')
	parser.add_argument('--cache', action='store_true', help='rebuild cache only')
	parser.add_argument('--input', type=str, help='input data file')
	parser.add_argument('--out', type=str, help='output cache folder')
	parser.add_argument('--user', type=str, help='user login name')
	parser.add_argument('--dbhost', type=str, help='database host name')
	parser.add_argument('--dbport', type=str, help='database port')
	parser.add_argument('--dbname', type=str, help='database name')
	parser.add_argument('--dbdrop', action='store_true', help='drop data for current user')
	parser.add_argument('--mapping', type=str, help='path to categories mapping file')
	parser.add_argument('--nitem', type=int, help='number of items to exoprt. -1 all')
	
	args = parser.parse_args()
	
	print("User %s"%args.user)
	
	# check attributes correctness
	if not hasattr(args, 'input'):
		raise Exception("No [input] attribute")
	
	if not hasattr(args, 'out'):
		raise Exception("No [out] attribute")
	
	if not hasattr(args, 'user'):
		raise Exception("No [user] attribute")
	
	if not hasattr(args, 'mapping'):
		raise Exception("No [mapping] attribute")
	
	data_folder = path.dirname(path.abspath(args.input)) + '/'
	data_filename = path.basename(args.input)
	out_path = path.abspath(args.out) + '/'
	resource_folder = out_path + '/' + args.user
	
	print('data folder:', data_folder)
	print('data filename:', data_filename)
	print('out folder', out_path)
	print('resource folder', resource_folder)

	specs = dict()
	
	specs['path'] = {
		'data':data_folder,
		'filename':data_filename,
		'mapping':args.mapping,
		'out':out_path,
		'res':resource_folder
    }
	specs['user'] = {'login':args.user}
	
	specs['db'] = {
        'host':args.dbhost,
        'port':args.dbport,
        'name':args.dbname,
        'dbdrop':args.dbdrop,
        'nitem':args.nitem,
        }
	
	specs['opt'] = {
		'nitem':args.nitem,
		}
	
	try:
		print("start script")
		
		cache = cache_data.CacheData(specs)
		
		build_cache = False

		if hasattr(args, 'all') or hasattr(args, 'cache'):
			build_cache = True
			
		if build_cache:	
			cache.cache()
	
		#build database
		builder = builder_db.BuilderDB(specs, cache)
		builder.build()
		
	except Exception:
		print(sys.exc_info()[0])
		print(sys.exc_info()[1]) 
		
	return 1
	
if __name__== "__main__":
	main()