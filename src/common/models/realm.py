from bson.objectid import ObjectId
import common.db.instance
from category_model import CategoryModel
from users_model import UsersModel
from user_groups_model import UserGroupsModel
from items_cache_model import ItemsCacheModel
from base_aspects_container import BaseAspectsContainer
from user_aspects_container import UserAspectsContainer
from category_group_items_cache import CategoryGroupItemsCache
from base_mapping import BaseMapping

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
        self.base_mapping = BaseMapping(self)
        pass

#----------------------------------------------------------------------------------------------
    def start(self):
        self.db.connect()
        
        self.base_aspects_container.load(self.category_group_items_cache)
        self.user_aspects_container.load(self.category_group_items_cache)
        
        self.category_group_items_cache.build_cache()
        self.base_mapping.load(self.specs['path']['data_dir'] + 'mapping.xml')

#----------------------------------------------------------------------------------------------
    def stop(self):
        self.db.disconnect()
        
#----------------------------------------------------------------------------------------------        
    def get_categories_1st_lvl(self, token, aspect):
        ''' empty aspect means user aspect'''
        res = []
        settings = self.users_model.get_user_settings(token)
        
        b_show_base_aspect_whole_tree = settings.options['client']['ui']['cases']['show_base_aspect_whole_tree']
        
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
                n_childs = self.category_group_items_cache.get_item_count(aspect, str(child.category._id), user_group_id)
                n_self_childs = self.category_group_items_cache.get_category_items_count_self(aspect, str(child.category._id), user_group_id)
                if b_show_base_aspect_whole_tree or n_childs > 0:
                    
                    n_show_childs = 0
                    if b_show_base_aspect_whole_tree:
                        n_show_childs = len(child.childs)
                    else:   
                        if n_self_childs == n_childs:
                            n_show_childs = 0
                        else:
                            n_show_childs = 1
                            
                    res.append({'_id':str(child.category._id), 
                            'parent_id': str(child.category.parent_id),
                            'name':child.category.name, 
                            'n_childs':str(n_show_childs)})
        return res

#----------------------------------------------------------------------------------------------    
    def get_category_childs(self, token, aspect, category_id):
        ''' empty aspect means user aspect'''
        res = []
        
        settings = self.users_model.get_user_settings(token)
        b_show_base_aspect_whole_tree = settings.options['client']['ui']['cases']['show_base_aspect_whole_tree']
        
        if aspect == '':
            res = self.users_model.get_child_categories(token, category_id)
        else:
            user_group_id = self.users_model.get_group_id_by_token(token)
            
            childs = self.base_aspects_container.get_aspect_child_categories(aspect, category_id)
            for child in childs:
                n_childs = self.category_group_items_cache.get_item_count(aspect, str(child.category._id), user_group_id)
                n_self_childs = self.category_group_items_cache.get_category_items_count_self(aspect, str(child.category._id), user_group_id)
                
                if b_show_base_aspect_whole_tree or n_childs > 0:
                    n_show_childs = 0
                    if b_show_base_aspect_whole_tree:
                        n_show_childs = len(child.childs)
                    else:   
                        if n_self_childs == n_childs:
                            n_show_childs = 0
                        else:
                            n_show_childs = 1
                
                    res.append({'_id':str(child.category._id), 
                            'parent_id': str(child.category.parent_id),
                            'name':child.category.name, 
                            'n_childs':str(n_show_childs)})
        return res
    
#----------------------------------------------------------------------------------------------
    def get_items(self, token, aspect, category_id, offset, count):
        ranges = []
        group_id = self.users_model.get_group_id_by_token(token)
        
        self.category_group_items_cache._get_base_categories_list_items(aspect, ObjectId(category_id), 
                                                                        group_id,
                                                                        offset, offset + count, ranges)
        #print('{}-{}'.format(offset, offset + count))
        #print ranges
        
        items = []
        for range in ranges:
            mappings = self.db.items_mapping.get_mappings_by_aspect_category(group_id, aspect, range[0], range[1], range[2])
            
            for mapping in mappings:
                item = self.items_cache_model.get_item(token, mapping['item_id'])
                if item:
                    items.append(item.get())
                else:
                    print('[Message_server_get_items] failed get item {}'.format(mapping['item_id']))
        return items

#----------------------------------------------------------------------------------------------
    def get_user_category_items(self, token, category_id, offset, count):
        items = []
        ranges = []
        
        self.category_group_items_cache._get_user_categories_list_items(ObjectId(category_id), 
                                                                        self.users_model.get_group_id_by_token(token),
                                                                        offset, offset + count, ranges)
        #print('{}-{}'.format(offset, offset + count))
        #print ranges
        
        for range in ranges:
            mappings = self.db.items_mapping.get_mappings_by_user_category(self.users_model.get_group_id_by_token(token), range[0], range[1], range[2])
        
            for mapping in mappings:
                item = self.items_cache_model.get_item(token, mapping['item_id'])
                if item:
                    items.append(item.get())
                else:
                    print('[Message_server_get_items] failed get item {}'.format(mapping['item_id']))
        return items
    
#----------------------------------------------------------------------------------------------
    def get_category_info(self, token, aspect, category_id):
        ''' retrieve items using cache '''
        print('get_category_info {} {}'.format(aspect, category_id))
        return {'items_num':self.category_group_items_cache.get_item_count(aspect, category_id, self.users_model.get_group_id_by_token(token))}
    
#----------------------------------------------------------------------------------------------
    def get_user_category_info(self, token, category_id):
        ''' retrieve items count from user category using cache '''
        return {'items_num':self.category_group_items_cache.get_user_category_items_count(category_id, self.users_model.get_group_id_by_token(token))}

#----------------------------------------------------------------------------------------------
    def addItem(self, 
                user_id,
                user_mapping,
                base_mapping,
                spec
                ):
        ''' add item to base. update runtime cache and mappings'''
        out = None
        user = self.realm.db.users.getUserById(user_id)
        if user:
            pass
        else:
            print('[addItem] failed get user: return None')
        
        return out

#----------------------------------------------------------------------------------------------
    def getBaseCategoryByPath(self, aspect, path_list):
        ''' Retrieve category by path. 
        @param path_list array on node names started from most top. root may be omitted.
        '''
        return self.base_aspects_container.getBaseCategoryByPath(aspect, path_list)