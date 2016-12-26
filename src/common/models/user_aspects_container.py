
from bson.objectid import ObjectId
from common.db.types.types import Category, UserAspect, User

DEFAULT_CATEGORY_NAME = 'All'

class UserAspectsContainer():
    def __init__(self, db_inst):
        self.db_inst = db_inst
        self.aspects = {}
        pass
    
#----------------------------------------------------------------------------------------------    
    def load(self, cache_ref):
        print('load user aspects')
        user_groups = cache_ref.realm().db.user_groups.get_all_groups()
        for group in user_groups:
            aspect = self.db_inst.user_aspects.get_aspect(group.aspect_id)
            
            if aspect and str(group._id) not in self.aspects:
                self.aspects[str(group._id)] = aspect
                
                # breath traverse aspect
                stack = []
                stack.append(aspect.node_root)

                while len(stack):      
                    new_stack = []
                    for item in stack:
                        cache_ref.add_user_category(group._id, str(item.category._id))
            
                        for child in item.childs:
                            new_stack.append(child)
                    stack = new_stack
            else:
                print('ERROR: user aspect already exist. try to reload')
        pass
    
#----------------------------------------------------------------------------------------------
    def get_aspect_category(self, group_id, category_id):
        out = None
        if self.aspects.get(str(group_id)):
            if str(category_id) in self.aspects[str(group_id)].hashmap:
                out = self.aspects[str(group_id)].hashmap[str(category_id)]
        return out
    
#----------------------------------------------------------------------------------------------    
    def get_aspect_default_category(self, group_id):
        out = None
        if self.aspects.get(str(group_id)):
            for child in self.aspects[str(group_id)].node_root.childs:
                if child.category.name == DEFAULT_CATEGORY_NAME:
                    out = child.category
                    break
        return out

