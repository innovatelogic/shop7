
USER_GROUPS_MAPPING_NAME = "user_category_mapping"

#----------------------------------------------------------------------------------------------
class GroupCategoryMapping():
    def __init__(self, instance):
        self.instance = instance
        
#----------------------------------------------------------------------------------------------
    def init(self):
        self.cat = self.instance.connection.db[USER_GROUPS_MAPPING_NAME]
        
#----------------------------------------------------------------------------------------------
    def getMapping(self, group_id):
        out = []
        return out
    
#----------------------------------------------------------------------------------------------
    def removeMapping(self, mapping_id):
        pass

#----------------------------------------------------------------------------------------------
    def addMapping(self, map_dict):
        pass
        
        