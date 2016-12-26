
import common.db.instance
import common.connection_db
from common.models.base_aspects_container import BaseAspectsContainer, CategoryNode, BaseAspectHelper
from common.db.types.types import Category
from opt import Opt

#----------------------------------------------------------------------------------------------            
def createNewUserWithGroup(params):
    print('Create New user With New group')
    spec = {}
    
    print('enter user email (login)')
    spec['email'] = raw_input().strip().lower()
    
    print('enter user name')
    spec['name'] = raw_input().strip().lower()
    
    print('enter password')
    spec['pwhsh'] = raw_input().strip().lower()
    
    print('enter user phone')
    spec['phone'] = raw_input().strip().lower()
    
    params.users.addUser(spec, None, 'all')
    
    return 1

#----------------------------------------------------------------------------------------------
def createNewUserWithinExistedGroup(params):
    print('Create New user within existed group')
    
    print('enter group id')
    group_id = raw_input().strip().lower()
    
    user_group = params.user_groups.get_user_group(group_id)
    if user_group:
        spec = {}
    
        print('enter user email (login)')
        spec['email'] = raw_input().strip().lower()
    
        print('enter user name')
        spec['name'] = raw_input().strip().lower()
    
        print('enter password')
        spec['pwhsh'] = raw_input().strip().lower()
    
        print('enter user phone')
        spec['phone'] = raw_input().strip().lower()
    
        params.users.addUser(spec, user_group, 'all')
    else:
        print('invalid user group')

    return 1

#----------------------------------------------------------------------------------------------
def operateUserManagement(params):
    opt = Opt({'1':('create New user with New group', createNewUserWithGroup, (params)),
               '2':('create New user within existed group', createNewUserWithinExistedGroup, (params))})
    opt.run()
    return 0