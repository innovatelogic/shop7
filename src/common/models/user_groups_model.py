import time

class UserGroupsModel():
    def __init__(self, db):
        self.db = db
        self.userGroupSessions = {}

#----------------------------------------------------------------------------------------------
    def loadUserGroupSession(self, group_id, token):
        if self.userGroupSessions.get(group_id):
            self.userGroupSessions[group_id]['refs'] += 1
        else:
            print(time.asctime(), "load user group")
            group = self.db.user_groups.get_user_group(group_id)
            aspect = self.db.user_aspects.get_aspect(group.aspect_id)
            mapping = self.db.group_category_mapping.loadUserMapping(group)
            self.userGroupSessions[group_id] = {'group':group, 'aspect':aspect, 'mapping':mapping, 'refs':1}

#----------------------------------------------------------------------------------------------            
    def releaseUserGroupSession(self, group_id):
        self.userGroupSessions[group_id]['refs'] -= 1
        
        if (self.userGroupSessions[group_id]['refs'] <= 0):
            del self.userGroupSessions[group_id]
            print(time.asctime(), "release user group")
   
#---------------------------------------------------------------------------------------------- 
    def get_first_level_categories(self, group_id):
        ''' return categories by id. integer means how levels will return '''
        out = []
        
        if self.userGroupSessions.get(group_id):            
            aspect = self.userGroupSessions[group_id]['aspect']
            root = aspect.node_root
            out.append({'_id':str(root.category._id), 
                        'parent_id': str(root.category.parent_id),
                        'name':root.category.name, 
                        'n_childs':str(len(root.childs))})
                
            for item in root.childs:
                out.append({'_id':str(item.category._id), 
                            'parent_id': str(item.category.parent_id),
                            'name':item.category.name, 
                            'n_childs':str(len(item.childs))})
                
        return out

#----------------------------------------------------------------------------------------------     
    def get_child_categories(self, group_id, str_parent_id):
        out = []
        if self.userGroupSessions.get(group_id):
            aspect = self.userGroupSessions[group_id]['aspect']
            node = aspect.hashmap[str_parent_id]
            for item in node.childs:
                out.append({'_id':str(item.category._id), 
                            'parent_id': str(item.category.parent_id),
                            'name':item.category.name, 
                            'n_childs':str(len(item.childs))})
                
        return out
    