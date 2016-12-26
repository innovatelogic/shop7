import os, sys, shutil, argparse
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from opt import Opt
import opt_operate_db
		
#----------------------------------------------------------------------------------------------
def main():
	reload(sys)
	
	sys.setdefaultencoding('utf8')

	parser = argparse.ArgumentParser()
	parser.add_argument('--dbhost', type=str, help='database host name')
	parser.add_argument('--dbport', type=str, help='database port')
	parser.add_argument('--dbname', type=str, help='database name')
	
	args = parser.parse_args()

	specs = {}
	specs['db'] = {
        'host':args.dbhost,
        'port':args.dbport,
        'name':args.dbname,
        }
	
	try:
		print("cmsc starting ...")
		
		opt = Opt({'1':('operate db', opt_operate_db.operateDB, specs), '2':('connect to MS', None)})
		opt.run()
		
		print("end script")
		
	except Exception:
		print(sys.exc_info()[0])
		print(sys.exc_info()[1]) 
		
	return 0

#----------------------------------------------------------------------------------------------
if __name__== "__main__":
	main()