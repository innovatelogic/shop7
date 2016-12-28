
import common.db.instance
import common.connection_db
from opt import Opt, variant
import opt_operate_users
import opt_operate_categories

#----------------------------------------------------------------------------------------------
def dropDB(params):
    print('confirm drop db Y/N ?')
    
    var = Opt.input()
    if var == 'y':
        params.drop()
    return 1

#----------------------------------------------------------------------------------------------
def operateDB(specs):
    db = common.db.instance.Instance(specs)
    db.connect()
    
    opt = Opt([variant('1','users management', opt_operate_users.operateUserManagement, db), 
               variant('2','categories management', opt_operate_categories.operateCategories, (specs, db)),
               variant('3','drop db', dropDB, db)])
    opt.run()