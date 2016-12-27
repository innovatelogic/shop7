
import common.db.instance
import common.connection_db
from common.models.base_aspects_container import BaseAspectsContainer, CategoryNode, BaseAspectHelper
from common.db.types.types import Category
from opt import Opt, variant
import opt_operate_users

#----------------------------------------------------------------------------------------------
def dropDB(params):
    print('drop db Y/N ?')
    
    var = Opt.input()
    if var == 'y':
        params.drop()
    

#----------------------------------------------------------------------------------------------
def operateDB(params):
    print('operate DB')
    print params
    db = common.db.instance.Instance(params)
    db.connect()
    
    opt = Opt([variant('1','users management', opt_operate_users.operateUserManagement, db), 
               variant('2','categories management'),
               variant('3','drop db', dropDB, db)])
    opt.run()