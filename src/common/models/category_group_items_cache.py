
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class CategoryGroupItemsCache():
    def __init__(self, realm):
        self.__realm = realm
        self._mapping = {}
        self._user_mapping = {}
        
#----------------------------------------------------------------------------------------------    
    def realm(self):
        return self.__realm
    
#----------------------------------------------------------------------------------------------        
    def build_cache(self):
        self.build(self.__realm.db.items.get_all_items(),
                   self.__realm.db.user_groups.get_all_groups())
    

#----------------------------------------------------------------------------------------------    
    def build(self, items, user_groups):
        
        base_aspects = self.__realm.base_aspects_container.get_aspects()
        
        for item in items:
            mapping = self.__realm.db.items_mapping.get_mapping(item.mapping_id)
            if mapping:
                b_mapped_usr_ctry = False
                for key, value in mapping.mapping.iteritems():
                    if key in base_aspects:
                        self.inc_item_count_base_aspect(key, value, item.user_group_id)
                    else:
                        self.inc_item_count_user_aspect(key, value)
                        b_mapped_usr_ctry = True

                if not b_mapped_usr_ctry: # default mapping
                    self.map_item_default_user_aspect(item.user_group_id)

#----------------------------------------------------------------------------------------------
    def add_base_category(self, aspect, category_id):
        str_category_id = str(category_id)
        
        if aspect not in self._mapping:
            self._mapping[aspect] = {}
        if category_id not in self._mapping[aspect]:
            self._mapping[aspect][category_id] = {}
        pass

#----------------------------------------------------------------------------------------------    
    def add_user_category(self, group_id, category_id):
        str_group_id = str(group_id)
        str_category_id = str(category_id)
        
        if str_group_id not in self._user_mapping:
            self._user_mapping[str_group_id] = {}
        if str_category_id not in self._user_mapping[str_group_id]:
            self._user_mapping[str_group_id][str_category_id] = 0 # zero count by default

#----------------------------------------------------------------------------------------------
    def get_item_count(self, aspect, category_id, group_id):
        out = 0
        if aspect in self._mapping:
            if str(group_id) in self._mapping[aspect][category_id]:
                out = self._mapping[aspect][category_id][group_id]
        return out
    
#----------------------------------------------------------------------------------------------    
    def inc_item_count_base_aspect(self, aspect, category_id, group_id):
        category_node = self.__realm.base_aspects_container.get_aspect_category(aspect, str(category_id))
        if category_node:
            while category_node:
                if str(group_id) not in self._mapping[aspect][category_node.category._id]: # add group if not exist
                    self._mapping[aspect][category_node.category._id][str(group_id)] = 0
                
                self._mapping[aspect][category_node.category._id][str(group_id)] += 1
           
                category_node = category_node.parent
        else:
            print('[inc_item_count_base_aspect] failed get category node') 
        pass
    
#----------------------------------------------------------------------------------------------    
    def inc_item_count_user_aspect(self, group_id, category_id):       
        category_node = self.__realm.user_aspects_container.get_aspect_category(group_id, category_id)
        if category_node:
            while category_node:
                self._user_mapping[str(group_id)][str(category_node.category._id)] += 1
                category_node = category_node.parent
        else:
            print('[inc_item_count_base_aspect] failed get category node') 
        pass
    
#----------------------------------------------------------------------------------------------    
    def map_item_default_user_aspect(self, group_id):
        default_category = self.__realm.user_aspects_container.get_aspect_default_category(group_id)
        if default_category:
            self.inc_item_count_user_aspect(group_id, default_category._id)
        else:
            print('[map_item_default_user_aspect] failed get category node') 
        pass