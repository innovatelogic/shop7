

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
    
    def get_count(self, category_id, group_id):
        return self.cache.get_count(category_id, group_id)

class CategoryGroupItemsCache():
    def __init__(self, realm):
        self.realm = realm
        self.mapping = {}
        
    def build_cache(self):
        user_groups = self.realm.db.user_groups.get_all_groups()
        items = self.realm.db.items.get_all_items()
        
        aspects = self.realm.base_aspects_container.get_aspects()
        
        for name in aspects:
            aspect = self.realm.base_aspects_container.get_aspect(name)
            if aspect:
                self.mapping[name] = AspectCache(self.realm, aspect, user_groups, items)
        pass
    
    def get_item_count(self, aspect, category_id, group_id):
        out = 0
        if aspect in self.mapping:
            out = self.mapping[aspect].get_count(category_id, group_id)
        return out