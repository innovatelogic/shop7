
USER_GROUPS_CATEGORY_NAME = 'user_groups'

class UserGroups():
    def __init__(self, connection):
        self.connection = connection
        
    def init(self):
        self.cat = self.connection.db[USER_GROUPS_CATEGORY_NAME]   
    
    def add_user_group(self, specs):
        pass
    
    def def_user_group(self, id):
        pass
    
    def modify_user_group(self, id, specs):
        pass