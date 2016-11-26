
#----------------------------------------------------------------------------------------------
class NodeCache():
    def __init__(self):
        self.hashmap = {}
        
    def add_mapping(self, category_id, group_id):
        str_category_id = str(category_id)
        str_group_id = str(group_id)
        
        if not str_category_id in self.hashmap:
            self.hashmap[str_category_id] = {}
        
        if not str_group_id in self.hashmap[str_category_id]:
            self.hashmap[str_category_id][str_group_id] = 0
        else:
            self.hashmap[str_category_id][str_group_id] += 1
        
    
    def get_count(self, category_id, group_id):
        out = 0
        if str(category_id) in self.hashmap:
            if str(group_id) in self.hashmap[str(category_id)]:
                out = self.hashmap[str(category_id)][str(group_id)]
        return out
    
#----------------------------------------------------------------------------------------------
class AspectCache():
    ''' cache contain aspect's category <-> items count for fast access'''
    def __init__(self, realm, aspect, user_groups, items):
        self.cache = NodeCache()
        self.build_aspect_cache(realm, aspect, user_groups, items)
        pass
    
    def build_aspect_cache(self, realm, aspect, user_groups, items):       
        for key, value in aspect.hashmap.iteritems():
            for item in items:
                mapping = realm.db.items_mapping.get_mapping(item.mapping_id)
                if mapping:
                    if aspect.name in mapping.mapping:
                        if str(key) == str(mapping.mapping[aspect.name]): #item is mapped to current category
                            self.cache.add_mapping(key, item.user_group_id)
                            # update ascender elements
                            parent = value.parent
                            while parent:
                                self.cache.add_mapping(parent.category._id, item.user_group_id)
                                parent = parent.parent
                else:
                    print('[build_aspect_cache] Error no mapping found {}'.format(item.mapping_id))
        pass

#----------------------------------------------------------------------------------------------    
    def get_count(self, category_id, group_id):
        return self.cache.get_count(category_id, group_id)

#----------------------------------------------------------------------------------------------
class CategoryGroupItemsCache():
    def __init__(self, realm):
        self.__realm = realm
        self.mapping = {}
        self._mapping = {}
        self._user_mapping = {}
        
#----------------------------------------------------------------------------------------------    
    def realm(self):
        return self.__realm
    
#----------------------------------------------------------------------------------------------        
    def build_cache(self):
        #aspects = self.__realm.base_aspects_container.get_aspects()
        
        #for name in aspects:
        #    aspect = self.__realm.base_aspects_container.get_aspect(name)
        #    if aspect:
        #        self.mapping[name] = AspectCache(self.__realm, aspect, user_groups, items)
        
        self.build(self.__realm.db.items.get_all_items(),
                   self.__realm.db.user_groups.get_all_groups())
    

#----------------------------------------------------------------------------------------------    
    def build(self, items, user_groups):
        
        base_aspects = self.__realm.base_aspects_container.get_aspects()
        
        for item in items:
            mapping = self.__realm.db.items_mapping.get_mapping(item.mapping_id)
            if mapping:
                for key, value in mapping.mapping.iteritems():
                    b_mapped = False
                    if key in base_aspects:
                        self.inc_item_count_base_aspect(key, value, item.user_group_id)

                        b_mapped = True
                    else:
                        self.inc_item_count_user_aspect(key, value)
                        b_mapped = True
                        
                    if not b_mapped: # default mapping
                        map_item_default_user_aspect(item)

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
        if aspect in self.mapping:
            out = self.mapping[aspect].get_count(category_id, group_id)
        return out
    
#----------------------------------------------------------------------------------------------    
    def inc_item_count_base_aspect(self, aspect, category_id, group_id):
        if str(group_id) not in self._mapping[aspect][category_id]:
            self._mapping[aspect][category_id][str(group_id)] = 0
        else:
           self._mapping[aspect][category_id][str(group_id)] += 1
        
        category_node = self.__realm.base_aspects_container.get_aspect_category(aspect, str(category_id))
        if category_node:
            parent = category_node.parent
            while parent:
                self.inc_item_count_base_aspect(aspect, parent.category._id, group_id)
                parent = parent.parent
        else:
            print('[inc_item_count_base_aspect] failed get category node') 
        pass
    
#----------------------------------------------------------------------------------------------    
    def inc_item_count_user_aspect(self, group_id, category_id):
        self._user_mapping[str(group_id)][str(category_id)] += 1
        pass
    
#----------------------------------------------------------------------------------------------    
    def map_item_default_user_aspect(self, item):
        pass