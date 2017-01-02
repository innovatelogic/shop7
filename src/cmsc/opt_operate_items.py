import common.db.instance
import common.plugins.import_prom_ua.importer
from opt import Opt, variant

#----------------------------------------------------------------------------------------------
def importUserItemsPromUA(params_tup):    
    print('enter user email (login)')
    user_name = Opt.input()
    
    db = params_tup[1]
    user = db.users.get_user_by_name(user_name)
    if user:
        user_group = db.user_groups.get_user_group(user.group_id)
        if user_group:
            print('input items filename (xlsx)')
            items_filename = Opt.input()
            
            importer = common.plugins.import_prom_ua.importer.Importer(params_tup[0], items_filename, user, user_group, db)
            importer.run()
            pass
        else:
            print('fail get user group')
    else:
        print('invalid user name')
            
    return 1

#----------------------------------------------------------------------------------------------
def importUserCategoryWithItemsPromUA(params):
    print('import items from prom_ua (with user categories)')
    return 1

#----------------------------------------------------------------------------------------------
def deleteItem(params):
    return 1

#----------------------------------------------------------------------------------------------
def deleteUserItems(params):
    return 1

#----------------------------------------------------------------------------------------------
def deleteAllItems(params):
    return 1

#----------------------------------------------------------------------------------------------
def operate(params):
    opt = Opt([variant('1','import user items from prom_ua', importUserItemsPromUA, params),
               variant('2', 'import user categories with items from prom_ua', importUserCategoryWithItemsPromUA, params),
               variant('3', 'delete item', deleteItem, params),
               variant('4', 'delete all user items', deleteUserItems, params),
               variant('5', 'delete all items', deleteAllItems, params)])
    opt.run()
    return 0