import os, sys, shutil, argparse
import codecs, json, io
from openpyxl import load_workbook
from bson.objectid import ObjectId
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from base_file_reader import BaseFileReader
from tree_loader import TreeLoader
import common.db.instance
from common.models.base_aspects_container import BaseAspectsContainer, BaseAspectHelper
from common.db.types.category import Category

#----------------------------------------------------------------------------------------------
def main():
	reload(sys)
	
	sys.setdefaultencoding('utf8')

	parser = argparse.ArgumentParser()
	
	parser.add_argument('--input', type=str, help='input data file')
	parser.add_argument('--out', type=str, help='output cache folder')
	parser.add_argument('--dbhost', type=str, help='database host name')
	parser.add_argument('--dbport', type=str, help='database port')
	parser.add_argument('--dbname', type=str, help='database name')
	parser.add_argument('--dbdrop', action='store_true', help='drop data for current user')
	parser.add_argument('--aspect', type=str, help='aspect import')
	
	args = parser.parse_args()
		
	# check attributes correctness
	if not hasattr(args, 'input'):
		raise Exception("No [input] attribute")
	
	if not hasattr(args, 'out'):
		raise Exception("No [out] attribute")
	
	data_folder = path.dirname(path.abspath(args.input)) + '/'
	data_filename = path.basename(args.input)
	out_path = path.abspath(args.out) + '/'
	
	print('data folder:', data_folder)
	print('data filename:', data_filename)
	print('out folder', out_path)
	
	specs = dict()
	
	specs['path'] = {
		'data':data_folder,
		'filename':data_filename,
		'out':out_path,
    }
	
	specs['db'] = {
        'host':args.dbhost,
        'port':args.dbport,
        'name':args.dbname,
        }
	
	specs['opt'] = {'aspect':args.aspect}
	
	try:
		print("start script")

		#base_file_reader = BaseFileReader(specs)
		#base_file_reader.read()
		#base_file_reader.save('test.xml')
		#return
	
		db = common.db.instance.Instance(specs)
		db.connect()
		
		ASPECT_ID = specs['opt']['aspect']
		
		aspect_src = BaseAspectHelper.loadFromXML(data_folder + data_filename)
		
		BaseAspectHelper.dump_category_tree(specs['path']['data'] + data_filename, aspect_src[0])

		db.base_aspects.clear(ASPECT_ID)
		#return
		
		if not db.base_aspects.isAspectExist(ASPECT_ID):
			db.base_aspects.cat.insert({'_id':ASPECT_ID})
		
		aspect_dst = BaseAspectHelper.load_aspect(ASPECT_ID, db, None)
		
		if not aspect_dst: #data_filename
			print('no aspect loaded. create root')
			db.base_aspects.add_category(ASPECT_ID, Category({'_id':ObjectId(), 'parent_id':None, 'name':'root', 'local':''}))
			aspect_dst = BaseAspectHelper.load_aspect(ASPECT_ID, db, None)

		BaseAspectHelper.treeMerge(aspect_src[0], aspect_dst.root)
		
		BaseAspectHelper.dump_category_tree(specs['path']['data'] + 'merge.tmp', aspect_dst.root)
		
		BaseAspectHelper.save_aspect(db, ASPECT_ID, aspect_dst.root)
		
		db.base_aspects.setDefaultCategoryName(ASPECT_ID, aspect_src[1])
		
		print("end script")
		
	except Exception:
		print(sys.exc_info()[0])
		print(sys.exc_info()[1]) 
		
	return 0
	
if __name__== "__main__":
	main()