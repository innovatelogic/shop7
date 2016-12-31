import common.db.instance
import common.connection_db
from opt import Opt, variant

#----------------------------------------------------------------------------------------------
def importUserItemsPromUA(params):
    print('import items from prom_ua')
    return 1

#----------------------------------------------------------------------------------------------
def importUserCategoryWithItemsPromUA(params):
    print('import items from prom_ua')
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