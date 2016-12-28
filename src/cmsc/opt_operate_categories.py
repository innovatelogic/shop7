from bson.objectid import ObjectId
import common.db.instance
import common.connection_db
from common.models.base_aspects_container import BaseAspectsContainer, CategoryNode, BaseAspectHelper
from common.db.types.types import Category
from opt import Opt, variant

#----------------------------------------------------------------------------------------------
def importBaseAspect(params_tup):
    print('input aspect name')
    aspect_name = Opt.input()
    
    print('input aspect filename')
    file_name = Opt.input()
    
    fullpath = params_tup[0]['path']['data'] + file_name
    aspect_src = BaseAspectHelper.loadFromXML(fullpath)
    
    if len(aspect_src):
        db = params_tup[1]
        
        if not db.base_aspects.isAspectExist(aspect_name):
            db.base_aspects.cat.insert({'_id':aspect_name})
        
        aspect_dst = BaseAspectHelper.load_aspect(aspect_name, db, None)
        
        if not aspect_dst: #data_filename
            print('no aspect loaded. create root')
            db.base_aspects.add_category(aspect_name, Category({'_id':ObjectId(), 'parent_id':None, 'name':'root', 'local':''}))
            aspect_dst = BaseAspectHelper.load_aspect(aspect_name, db, None)

        BaseAspectHelper.treeMerge(aspect_src[0], aspect_dst.root)
        
        BaseAspectHelper.save_aspect(db, aspect_name, aspect_dst.root)
        
        db.base_aspects.setDefaultCategoryName(aspect_name, aspect_src[1])
        
        print('import finished')
    else:
        print('failed to load {} filename'.format(fullpath))
    return 1

#----------------------------------------------------------------------------------------------
def clearBaseAspect(params_tup):
    print('input aspect name')
    aspect_name = Opt.input()
    
    db = params_tup[1]
    if not db.base_aspects.isAspectExist(aspect_name):
        print ('aspect {} does not exist'.format(aspect_name))
    else:
        print('confirm Y/N ?')
        if Opt.input() == 'y':
            db.base_aspects.removeAspect(aspect_name)
            
#----------------------------------------------------------------------------------------------
def createUserCategory(paramd_tup):
    print('input user name')
    user_name = Opt.input()
    
    db = params_tup[1]
    user = db.users.get_user_by_name(user_name)
    if user:
        user_group = db.user_groups.get_user_group(user.group_id)
        if user_group:
            aspect = db.user_aspects.get_aspect(user.aspect_id)
            if aspect:
                print('input parent category id')
                parent_id = Opt.input()
        
            else:
                print('failed to get user aspect')
        else:
            print('fail get user group')
        
        
    else:
        print('invalid user name')
    return 1

#----------------------------------------------------------------------------------------------
def operateCategories(params_tup):
    opt = Opt([variant('1', 'import base aspect', importBaseAspect, params_tup),
               variant('2', 'clear base aspect', clearBaseAspect, params_tup),
               variant('3', 'create user category', createUserCategory, params_tup),
               variant('4', 'create user mapping'),
               variant('5', 'remove user mapping'),
               variant('6', 'clear user mapping')])
    opt.run()
    return 0