import time

class GroupsModel():
    def __init__(self, db_instance):
        self.db_instance = db_instance
        self.userGroupSessions = {}

#----------------------------------------------------------------------------------------------    
    def loadUserGroupSession(self, group_id, token):
        if self.userGroupSessions.get(group_id):
            self.userGroupSessions[group_id]['refs'] += 1
        else:
            print(time.asctime(), "load user group")
            new_group = self.db_instance.user_groups.get_user_group(group_id)
            aspect = self.db_instance.user_aspects.get_aspect(new_group.aspect_id)
            
            spec = {'group':new_group, 'aspect':aspect, 'refs':1}
            self.userGroupSessions[group_id] = spec

            
#----------------------------------------------------------------------------------------------            
    def releaseUserGroupSession(self, group_id):
        self.userGroupSessions[group_id]['refs'] -= 1
        
        if (self.userGroupSessions[group_id]['refs'] <= 0):
            del self.userGroupSessions[group_id]
            print(time.asctime(), "release user group")
    