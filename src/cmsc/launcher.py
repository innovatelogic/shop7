import os, sys, shutil, argparse
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from opt import Opt, variant
import opt_operate_db
		
#----------------------------------------------------------------------------------------------
def main():
	reload(sys)
	
	sys.setdefaultencoding('utf8')

	parser = argparse.ArgumentParser()
	parser.add_argument('--dbhost', type=str, help='database host name')
	parser.add_argument('--dbport', type=str, help='database port')
	parser.add_argument('--dbname', type=str, help='database name')
	parser.add_argument('--input', type=str, help='input data folder')
	
	args = parser.parse_args()

	specs = {}
	specs['db'] = {
        'host':args.dbhost,
        'port':args.dbport,
        'name':args.dbname,
        }
	
	data_folder = path.abspath(args.input) + '/'
	
	specs['path'] = {
		'data':data_folder,
		'data_dir':data_folder,
    }
	
	try:
		print("cmsc starting ...")
		
		print('data folder:', data_folder)
		
		opt = Opt([variant('1', 'operate db', opt_operate_db.operate, specs), 
				   variant('2', 'connect to MS'),
				   variant('3', 'run UT')])
		opt.run()
		
		print("end script")
		
	except Exception:
		print(sys.exc_info()[0])
		print(sys.exc_info()[1]) 
		
	return 0

#----------------------------------------------------------------------------------------------
if __name__== "__main__":
	main()