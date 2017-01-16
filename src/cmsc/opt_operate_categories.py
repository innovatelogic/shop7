from bson.objectid import ObjectId
import common.db.instance
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

        BaseAspectHelper.treeMerge(aspect_dst.root, aspect_src[0])
        
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
def createUserCategory(params_tup):
    print('input user name')
    user_name = Opt.input()
    
    db = params_tup[1]
    user = db.users.get_user_by_name(user_name)
    if user:
        user_group = db.user_groups.get_user_group(user.group_id)
        if user_group:
            user_aspect = db.user_aspects.get_aspect(user_group.aspect_id)
            if user_aspect:
                print('input parent user category id')
                parent_id = Opt.input()
        
                parent_node = user_aspect.getCategoryNodeById(parent_id)
                if parent_node:
                    
                    print('input new category name')
                    new_name = Opt.input()

                    new_category = Category({'_id': ObjectId(), 'parent_id': parent_node.category._id, 'name':new_name})
                    
                    if user_aspect.addChildCategory(parent_node, new_category):
                        db.user_aspects.add_category(user_aspect._id, new_category)
                    else:
                        print('faied to add category ')
                else:
                    print('failed to get user parent_node')
                
            else:
                print('failed to get user aspect')
        else:
            print('fail get user group')
    else:
        print('invalid user name')
    return 1

#----------------------------------------------------------------------------------------------
def removeUserCategory(params_tup):
    print('input user name')
    user_name = Opt.input()
    
    db = params_tup[1]
    user = db.users.get_user_by_name(user_name)
    if user:
        user_group = db.user_groups.get_user_group(user.group_id)
        if user_group:
            user_aspect = db.user_aspects.get_aspect(user_group.aspect_id)
            if user_aspect:
                print('input user category id')
                category_id = Opt.input()
        
                category_node = user_aspect.getCategoryNodeById(category_id)
                if category_node:
                    if user_aspect.removeCategory(category_node):
                        out = db.user_aspects.removeCategory(user_aspect._id, category_node.category)
                        print('remove category ok {}'.format(out))
                    else:
                        print('faied to remove category ')
                else:
                    print('failed to get user parent_node')
                
            else:
                print('failed to get user aspect')
        else:
            print('fail get user group')
    else:
        print('invalid user name')

#----------------------------------------------------------------------------------------------
def createUserMapping(params_tup):
    print('input user name')
    user_name = Opt.input()
    
    db = params_tup[1]
    user = db.users.get_user_by_name(user_name)
    if user:
        user_group = db.user_groups.get_user_group(user.group_id)
        if user_group:
            user_aspect = db.user_aspects.get_aspect(user_group.aspect_id)
            if user_aspect:
                print('input user category id')
                category_id = Opt.input()
                
                user_category_node = user_aspect.getCategoryNodeById(category_id)
                if user_category_node:
                    print('input base aspect name')
                    aspect_name = Opt.input()
                    
                    if db.base_aspects.isAspectExist(aspect_name):
                        aspect_dst = BaseAspectHelper.load_aspect(aspect_name, db, None)
                        
                        print('input category id')
                        base_category_id = Opt.input()
                        
                        base_category_node = aspect_dst.getCategoryNodeById(base_category_id)
                        
                        if base_category_node:
                            mapping = db.group_category_mapping.getMapping(user_group)
                            if mapping and db.group_category_mapping.addUserMappingCategory(mapping, 
                                                                                            user_category_node.category, 
                                                                                            aspect_name, base_category_node.category):
                                db.group_category_mapping.updateUserMapping(mapping)
                                print('mapping added ok')
                            else:
                                print('mapping added fail')  
                        else:
                            print('failed to get base aspect category')
                    else:
                        print('aspect does not exist')
                else:
                    print('failed to get user category')
            else:
                print('failed to get user aspect')
        else:
            print('fail get user group')
    else:
        print('invalid user name')            
    pass

#----------------------------------------------------------------------------------------------
def removeUserMapping(params_tup):
    print('input user name')
    user_name = Opt.input()

    db = params_tup[1]
    user = db.users.get_user_by_name(user_name)
    if user:
        user_group = db.user_groups.get_user_group(user.group_id)
        if user_group:
            user_aspect = db.user_aspects.get_aspect(user_group.aspect_id)
            if user_aspect:
                print('input user category id')
                category_id = Opt.input()
                
                user_category_node = user_aspect.getCategoryNodeById(category_id)
                if user_category_node:
                    print('input base aspect name')
                    aspect_name = Opt.input()

                    mapping = db.group_category_mapping.getMapping(user_group)
                    db.group_category_mapping.removeUserMappingCategory(mapping, user_category_node.category, aspect_name)
                    db.group_category_mapping.updateUserMapping(mapping)
                else:
                    print('failed to get user category')
            else:
                print('failed to get user aspect')
        else:
            print('fail get user group')
    else:
        print('invalid user name')
        
#----------------------------------------------------------------------------------------------
def clearUserMapping(params_tup):
    print('input user name')
    user_name = Opt.input()

    db = params_tup[1]
    user = db.users.get_user_by_name(user_name)
    if user:
        user_group = db.user_groups.get_user_group(user.group_id)
        if user_group:
            user_aspect = db.user_aspects.get_aspect(user_group.aspect_id)
            if user_aspect:
                mapping = db.group_category_mapping.getMapping(user_group)
                db.group_category_mapping.clearUserMapping(mapping)
                db.group_category_mapping.updateUserMapping(mapping)
            else:
                print('failed to get user aspect')
        else:
            print('fail get user group')
    else:
        print('invalid user name')
      
#----------------------------------------------------------------------------------------------
def operate(params_tup):
    opt = Opt([variant('1', 'import base aspect', importBaseAspect, params_tup),
               variant('2', 'clear base aspect', clearBaseAspect, params_tup),
               variant('3', 'create user category', createUserCategory, params_tup),
               variant('4', 'remove user category', removeUserCategory, params_tup),
               variant('5', 'add user mapping', createUserMapping, params_tup),
               variant('6', 'remove user mapping', removeUserMapping, params_tup),
               variant('7', 'clear user mapping', clearUserMapping, params_tup)])
    opt.run()
    return 0