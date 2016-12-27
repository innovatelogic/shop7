
import common.db.instance
import common.connection_db
from common.models.base_aspects_container import BaseAspectsContainer, CategoryNode, BaseAspectHelper
from common.db.types.types import Category
from opt import Opt
import opt_operate_users
    

#----------------------------------------------------------------------------------------------
def operateDB(params):
    print('operate DB')
    print params
    db = common.db.instance.Instance(params)
    db.connect()
    
    print('red')
    opt = Opt({'1':('users management', opt_operate_users.operateUserManagement, db), 
               '2':('categories management', None),
               '3':('drop db', None)})
    opt.run()