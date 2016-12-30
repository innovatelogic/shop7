from types.types import UserMapping

USER_GROUPS_MAPPING_NAME = "user_category_mapping"

#----------------------------------------------------------------------------------------------
class GroupCategoryMapping():
    def __init__(self, instance):
        self.instance = instance
        
#----------------------------------------------------------------------------------------------
    def init(self):
        self.cat = self.instance.connection.db[USER_GROUPS_MAPPING_NAME]
        
#----------------------------------------------------------------------------------------------
    def getMapping(self, group):
        data = self.cat.find_one({'group_id':group._id})
        if data:
            return UserMapping(data)
        return None
    
#----------------------------------------------------------------------------------------------
    def removeMapping(self, userMapping):
        out = False
        if userMapping:
            self.cat.remove({"_id":userMapping._id})
            out = True
        return out

#----------------------------------------------------------------------------------------------
    def addMapping(self, userMapping):
        self.cat.insert(userMapping.get())
        pass
    
#----------------------------------------------------------------------------------------------
    def loadUserMapping(self, group):
        return self.getMapping(group)

#----------------------------------------------------------------------------------------------
    def addUserMappingCategory(self, user, user_category, aspect_name, category):
        pass

#----------------------------------------------------------------------------------------------
    def removeUserMapping(self, user, user_category, aspect_name, category):
        pass
    
#----------------------------------------------------------------------------------------------
    def clearUserMapping(self, user, user_category):
        pass
        
#----------------------------------------------------------------------------------------------
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()    