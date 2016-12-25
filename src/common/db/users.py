from types.types import User, UserRecord, UserGroup
from user_groups import UserGroups
from bson.objectid import ObjectId

USERS_CATEGORY_NAME = 'users'

class Users():
    def __init__(self, instance):
        self.instance = instance

#----------------------------------------------------------------------------------------------
    def init(self):
        self.cat = self.instance.connection.db[USERS_CATEGORY_NAME]

#----------------------------------------------------------------------------------------------
    def add_user(self, spec, group_id, rights):
        '''add new user. if group_id = None create new user group with user admin rights 
           otherwise group_id and rights should be set
           @return boolean value'''
        
        UNIQUE_FIELD_NAME = 'email'
        
        out = False
        if not self.get_user_by_name(spec[UNIQUE_FIELD_NAME]):
            if group_id:
                group = self.instance.user_groups.get_user_group(group_id)
                if group:
                    spec['_id'] = ObjectId()
                    spec['group_id'] = group._id
                    
                    new_user = User(spec)
                    self.cat.insert(new_user.get())
                    
                    group.records[str(spec['_id'])] = rights
                    self.instance.user_groups.update_user_group(group)
                    
                else:
                    print('[Users::add_user] failed get group %s'%str(group_id))
            else:
                # no group_id, create group and assign user to it
                
                  
                user_spec['_id'] = str(ObjectId())
                user_spec['group_id'] = str(ObjectId())
                
                spec_group = {'_id':str(spec['group_id'])}             
                spec_group['records'] = []
                spec_group['records'].append(UserRecord(user_spec['_id'], rights))
                
                new_group = UserGroup(spec_group)
                
                # TODO check spec valid?
                new_user = User(user_spec)
                
                self.instance.user_groups.add_user_group(new_group)
                self.cat.insert(new_user.get())
                
                out = True
        else:
            print('[Users::add_user] user {} already exist'.format(user_spec['email']))
            
        return out

#----------------------------------------------------------------------------------------------
    def remove_user(self, id):
        ''' removes user by id. cause modifying user group and remove it if necessary'''
        out = False
        data = self.cat.find_one({'_id':id})
        
        if data:
            res = self.instance.user_groups.remove_user_from_group(data['group_id'], data['_id'])
            self.cat.remove({"_id": data['_id']})
            out = True
        else:
            print("[Users::del_user] user {} dont exist".format(id))
        return out

#----------------------------------------------------------------------------------------------
    def modify_user(self, id, spec):
        pass

#----------------------------------------------------------------------------------------------
    def getUserById(self, _id):
        data = self.cat.find_one({'_id':_id})
        if data:
            return User(data)
        return None

#----------------------------------------------------------------------------------------------
    def get_user_by_name(self, login):
        data = self.cat.find_one({'email':login})
        if data:
            return User(data)
        return None

#----------------------------------------------------------------------------------------------
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()