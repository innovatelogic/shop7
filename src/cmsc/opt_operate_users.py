
import common.db.instance
import common.connection_db
from common.models.base_aspects_container import BaseAspectsContainer, CategoryNode, BaseAspectHelper
from common.db.types.types import Category
from opt import Opt, variant

#----------------------------------------------------------------------------------------------            
def createNewUserWithGroup(params):
    print('Create New user With New group')
    spec = {}
    
    print('enter user email (login)')
    spec['email'] = Opt.input()
    
    print('enter user name')
    spec['name'] = Opt.input()
    
    print('enter password')
    spec['pwhsh'] = Opt.input()
    
    print('enter user phone')
    spec['phone'] = Opt.input()
    
    params.users.addUser(spec, None, 'all')
    
    return 1

#----------------------------------------------------------------------------------------------
def createNewUserWithinExistedGroup(params):
    print('Create New user within existed group')
    
    print('enter group id')
    group_id = Opt.input()
    
    user_group = params.user_groups.get_user_group(group_id)
    if user_group:
        spec = {}
    
        print('enter user email (login)')
        spec['email'] = Opt.input()
    
        print('enter user name')
        spec['name'] = Opt.input()
    
        print('enter password')
        spec['pwhsh'] = Opt.input()
    
        print('enter user phone')
        spec['phone'] = Opt.input()
    
        params.users.addUser(spec, user_group, 'all')
    else:
        print('invalid user group')

    return 1

#----------------------------------------------------------------------------------------------
def deleteUser(params):
    print('enter user email (login)')
    name = Opt.input()
    
    user = params.users.get_user_by_name(name)
    if user:
        params.users.removeUser(user)
    else:
        print('invalid user name')
    return 1

#----------------------------------------------------------------------------------------------
def deleteUserGroup(params):
    spec = {}
    print('enter group id')
    group_id = Opt.input()
    
    user_group = params.user_groups.get_user_group(group_id)
    if user_group:
        params.user_groups.removeGroup(user_group)
    else:
        print('invalid user group')
    return 1

#----------------------------------------------------------------------------------------------
def operateUserManagement(params):
    opt = Opt([variant('1','create New user with New group', createNewUserWithGroup, params),
               variant('2', 'create New user within existed group', createNewUserWithinExistedGroup, params),
               variant('3', 'remove user', deleteUser, params),
               variant('4', 'remove user group', deleteUserGroup, params)])
    opt.run()
    return 0