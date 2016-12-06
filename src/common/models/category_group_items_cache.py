
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class CategoryGroupItemsCache():
    IDX_SELF_COUNTER = 0
    IDX_COMMON_COUNTER = 1
    
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
        ''' iterates through all items and assing counter to corresponding category node
            and all ancestors
        '''
        base_aspects = self.__realm.base_aspects_container.get_aspects()
        
        for item in items:
            mapping = self.__realm.db.items_mapping.get_mapping(item.mapping_id)
            if mapping:
                b_mapped_usr_ctry = False
                for key, value in mapping.mapping.iteritems(): # key - aspect; value - category_id
                    if key in base_aspects:
                        self.inc_item_count_base_aspect(key, value, item.user_group_id)
                    else:
                        self.inc_item_count_user_aspect(key, value)
                        b_mapped_usr_ctry = True

                if not b_mapped_usr_ctry: # default mapping
                    self.map_item_default_user_aspect(item.user_group_id)

#----------------------------------------------------------------------------------------------
    def add_base_category(self, aspect, category_id):
        #str_category_id = str(category_id)
        
        if aspect not in self._mapping:
            self._mapping[aspect] = {}
        if category_id not in self._mapping[aspect]:
            self._mapping[aspect][category_id] = {}
        pass

#----------------------------------------------------------------------------------------------    
    def add_user_category(self, group_id, category_id):
        str_group_id = str(group_id)
        str_category_id = str(category_id)
        
        if group_id not in self._user_mapping:
            self._user_mapping[group_id] = {}
        if str_category_id not in self._user_mapping[group_id]:
            self._user_mapping[group_id][category_id] = [0, 0] # zero count by default

#----------------------------------------------------------------------------------------------
    def get_item_count(self, aspect, category_id, group_id):
        out = 0
        if aspect in self._mapping:
            if group_id in self._mapping[aspect][category_id]:
                out = self._mapping[aspect][category_id][group_id][self.IDX_COMMON_COUNTER]
        return out
    
#----------------------------------------------------------------------------------------------
    def get_category_items_count_self(self, aspect, category_id, group_id):
        out = 0
        if aspect in self._mapping:
            if group_id in self._mapping[aspect][category_id]:
                out = self._mapping[aspect][category_id][group_id][self.IDX_SELF_COUNTER]
        return out

#----------------------------------------------------------------------------------------------   
    def get_user_category_items_count(self, category_id, group_id):
        return self._user_mapping[group_id][category_id][self.IDX_COMMON_COUNTER]
    
#----------------------------------------------------------------------------------------------    
    def inc_item_count_base_aspect(self, aspect, category_id, group_id):
        base_node = True
        category_node = self.__realm.base_aspects_container.get_aspect_category(aspect, str(category_id))
        if category_node:
            while category_node:
                if group_id not in self._mapping[aspect][str(category_node.category._id)]: # add group if not exist
                    self._mapping[aspect][str(category_node.category._id)][group_id] = [0, 0] # first element : self items counter, 
                                                                                              # second : self + descendants
                if base_node:
                    self._mapping[aspect][str(category_node.category._id)][group_id][self.IDX_SELF_COUNTER] += 1
                    base_node = False
                    
                self._mapping[aspect][str(category_node.category._id)][group_id][self.IDX_COMMON_COUNTER] += 1
                category_node = category_node.parent
        else:
            print('[inc_item_count_base_aspect] failed get category node') 
        pass
    
#----------------------------------------------------------------------------------------------    
    def inc_item_count_user_aspect(self, group_id, category_id):   
        base_node = True    
        category_node = self.__realm.user_aspects_container.get_aspect_category(group_id, category_id)
        if category_node:
            while category_node:
                if base_node:
                    self._user_mapping[group_id][str(category_node.category._id)][self.IDX_SELF_COUNTER] += 1
                    base_node = False
                self._user_mapping[group_id][str(category_node.category._id)][self.IDX_COMMON_COUNTER] += 1
                category_node = category_node.parent
        else:
            print('[inc_item_count_base_aspect] failed get category node') 
        pass
    
#----------------------------------------------------------------------------------------------    
    def map_item_default_user_aspect(self, group_id):
        default_category = self.__realm.user_aspects_container.get_aspect_default_category(group_id)
        if default_category:
            self.inc_item_count_user_aspect(group_id, str(default_category._id))
        else:
            print('[map_item_default_user_aspect] failed get category node') 
        pass
    
#----------------------------------------------------------------------------------------------    
    def get_base_categories_leaves_items_range(self, aspect, category_id, group_id, _min, _max):
        ''' retrieve list of {leaf_category_id: {offset: count_items_get}} corresponds to request '''
        out_list = []
        
        if _max > _min:
            if _max - _min > 50: # max 50 items
                _max = _min + 50
        
            self._get_base_categories_list_items(self, aspect, category_id, group_id, offset, max_count, out_list)
        
        return out_list
    
#----------------------------------------------------------------------------------------------    
    def _get_base_categories_list_items(self, aspect, category_id, group_id, _min, _max, out_list):
        ''' traverse tree in straight order to retrieve list of categories contains range of items
        return array of tuples (category_id, count, offset) 
        '''
        category_node = self.__realm.base_aspects_container.get_aspect_category(aspect, str(category_id))
        if category_node:
            stack = []
            stack.append(category_node)
            
            count_n = 0 # plain counter
            
            while len(stack):
                top = stack.pop(0)
                
                count_self = self.get_category_items_count_self(aspect, str(top.category._id), group_id)
                
                count_next = count_n + count_self
                if count_next > _min: # check threshold overstep
                    
                    count_get = min((count_next) - _min, _max - _min) #check _max cap
                    
                    offset = 0
                    if _min < count_next:
                        offset = count_self - count_get # offset from begin
                    
                    out_list.append((top.category._id, count_get, offset))
                    
                    _min = count_next
                    
                    if _min >= _max:
                        break
                    
                count_n += count_self
                
                for child in reversed(top.childs):
                    if self.get_item_count(aspect, str(child.category._id), group_id):
                        stack.insert(0, child)