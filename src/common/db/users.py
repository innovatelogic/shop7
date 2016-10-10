from types import User

USERS_CATEGORY_NAME = 'users'

class Users():
    def __init__(self, connection):
        self.connection = connection
        
    def init(self):
        self.cat = self.connection.db[USERS_CATEGORY_NAME]
        
    def add_user(self, spec, group_id):
        pass
    
    def del_user(self, id):
        pass
    
    def modify_user(self, id, spec):
        pass
        
    def get_user_by_name(self, login):
        data = self.cat.find_one({'email':login})
        if data:
            return User(data)
        return None
            