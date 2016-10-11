from types.types import User, UserRecord, UserGroup
from user_groups import UserGroups
from bson.objectid import ObjectId


USERS_CATEGORY_NAME = 'users'

class Users():
    def __init__(self, instance):
        self.instance = instance
        
    def init(self):
        self.cat = self.instance.connection.db[USERS_CATEGORY_NAME]
        
    def add_user(self, spec, group_id = None, rights = None):
        '''add new user. if group_id = None create new user group with user admin rights 
           otherwise group_id and rights should be set
           return boolean value'''
        
        out = False
        if not self.get_user_by_name(spec['email']):
            if group_id:
                group = self.instance.user_groups.get_user_group(group_id)
                if group:
                    spec['_id'] = ObjectId()
                    spec['group_id'] = group._id
                    
                    new_user = User(spec)
                    
                    self.cat.insert(new_user.get())
                    
                    group.records[str(spec['_id'])] = 'rw++'
                    
                    print 'ddd'
                    print group.records
                    
                    self.instance.user_groups.update_user_group(group)
                    
                else:
                    print('[Users::add_user] failed get group %s'%str(group_id))
            else:
                # no group_id, create group and assign user to it    
                spec['_id'] = str(ObjectId())
                group_spec = {'_id':str(ObjectId())}
                
                spec['group_id'] = group_spec['_id']
                
                group_spec['records'] = []
                group_spec['records'].append(UserRecord(spec['_id'], "rw+"))
                
                new_group = UserGroup(group_spec)
                
                # TODO check spec valid?
                new_user = User(spec)
                
                self.instance.user_groups.add_user_group(new_group)
                self.cat.insert(new_user.get())
                
                out = True
        else:
            print('[Users::add_user] user %s already exist'%spec['email'])
        
        return out
    
    def del_user(self, id):
        pass
    
    def modify_user(self, id, spec):
        pass
        
    def get_user_by_name(self, login):
        data = self.cat.find_one({'email':login})
        if data:
            return User(data)
        return None
    
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()