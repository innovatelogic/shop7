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
    def addUserMappingCategory(self, mapping, user_category, aspect_name, aspect_category):
        res = False
        if mapping and user_category and aspect_category:
            mapping.add(user_category._id, aspect_name, aspect_category._id)
            res = True
        return res
        
#----------------------------------------------------------------------------------------------
    def removeUserMappingCategory(self, mapping, user_category, base_aspect_name):
        res = False
        if mapping and user_category:
            res = mapping.remove(user_category._id, base_aspect_name)
        return res
    
#----------------------------------------------------------------------------------------------
    def clearUserMapping(self, mapping):
        mapping.clear()
        pass
    
#----------------------------------------------------------------------------------------------
    def updateUserMapping(self, mapping):
        self.cat.update_one({
          '_id': mapping._id
        },{
          '$set': {
            'mapping': mapping.mapping
          }
        }, upsert=False)

#----------------------------------------------------------------------------------------------
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()    