
import common.db.instance
import common.connection_db
from opt import Opt, variant
import opt_operate_users
import opt_operate_categories
import opt_operate_items

#----------------------------------------------------------------------------------------------
def dropDB(params):
    print('confirm drop db Y/N ?')
    
    var = Opt.input()
    if var == 'y':
        params.drop()
    return 1

#----------------------------------------------------------------------------------------------
def operate(specs):
    db = common.db.instance.Instance(specs)
    db.connect()
    
    opt = Opt([variant('1','users/group management', opt_operate_users.operate, db), 
               variant('2','categories management', opt_operate_categories.operate, (specs, db)),
               variant('3','items management', opt_operate_items.operate, (specs, db)),
               variant('4','drop db', dropDB, db)])
    opt.run()