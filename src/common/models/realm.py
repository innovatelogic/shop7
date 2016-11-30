from bson.objectid import ObjectId
import common.db.instance
from category_model import CategoryModel
from users_model import UsersModel
from user_groups_model import UserGroupsModel
from items_cache_model import ItemsCacheModel
from base_aspects_container import BaseAspectsContainer
from user_aspects_container import UserAspectsContainer
from category_group_items_cache import CategoryGroupItemsCache

class Realm():
    def __init__(self, specs):
        self.specs = specs
        self.db = common.db.instance.Instance(self.specs)
        self.category_model = CategoryModel(self.db)
        self.users_model = UsersModel(self.db, UserGroupsModel(self.db))
        self.items_cache_model = ItemsCacheModel(self.db)
        self.category_group_items_cache = CategoryGroupItemsCache(self)
        self.base_aspects_container = BaseAspectsContainer(self.db)
        self.user_aspects_container = UserAspectsContainer(self.db)
        pass

#----------------------------------------------------------------------------------------------
    def start(self):
        self.db.connect()
        
        self.base_aspects_container.load(self.category_group_items_cache)
        self.user_aspects_container.load(self.category_group_items_cache)
        
        self.category_group_items_cache.build_cache()

#----------------------------------------------------------------------------------------------
    def stop(self):
        self.db.disconnect()
        
#----------------------------------------------------------------------------------------------        
    def get_categories_1st_lvl(self, token, aspect):
        ''' empty aspect means user aspect'''
        res = []
        settings = self.users_model.get_user_settings(token)
        
        if aspect == '':
            res = self.users_model.get_first_level_categories(token)
        else:
            user_group_id = self.users_model.get_group_id_by_token(token)
            category_root = self.base_aspects_container.get_aspect_category_root(aspect)
            
            res.append({'_id':str(category_root.category._id), 
                        'parent_id': str(category_root.category.parent_id),
                        'name':category_root.category.name, 
                        'n_childs':str(len(category_root.childs))})
            
            childs = self.base_aspects_container.get_aspect_child_categories(aspect, category_root.category._id)
            
            for child in childs:
                if settings.options['client']['ui']['cases']['show_base_aspect_whole_tree'] or self.category_group_items_cache.get_item_count(aspect, child.category._id, user_group_id) > 0:
                    res.append({'_id':str(child.category._id), 
                            'parent_id': str(child.category.parent_id),
                            'name':child.category.name, 
                            'n_childs':str(len(child.childs))})
        return res

#----------------------------------------------------------------------------------------------    
    def get_category_childs(self, token, aspect, category_id):
        ''' empty aspect means user aspect'''
        res = []
        
        settings = self.users_model.get_user_settings(token)
        
        if aspect == '':
            res = self.users_model.get_child_categories(token, category_id)
        else:
            user_group_id = self.users_model.get_group_id_by_token(token)
            
            childs = self.base_aspects_container.get_aspect_child_categories(aspect, category_id)
            for child in childs:
                if settings.options['client']['ui']['cases']['show_base_aspect_whole_tree'] or self.category_group_items_cache.get_item_count(aspect, child.category._id, user_group_id) > 0:
                    res.append({'_id':str(child.category._id), 
                            'parent_id': str(child.category.parent_id),
                            'name':child.category.name, 
                            'n_childs':str(len(child.childs))})

        return res
    
#----------------------------------------------------------------------------------------------    
    def get_items(self, token, aspect, category_id):
        items = []
        mappings = self.db.items_mapping.get_mappings_by_aspect_category(aspect, category_id)
        
        for mapping in mappings:
            item = self.items_cache_model.get_item(token, mapping['item_id'])
            if item:
                items.append(item.get())
            else:
                print('[Message_server_get_items] failed get item {}'.format(mapping['item_id']))
                
        out = []
        self.category_group_items_cache.get_base_categories_list_items(aspect, ObjectId(category_id), self.users_model.get_group_id_by_token(token), 0, 10, out)
        print out
        return items

#----------------------------------------------------------------------------------------------    
    def get_items_ex(self, token, aspect, category_id, offset, max_count):
        ''' retrieve items using cache '''
        
        pass