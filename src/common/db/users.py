from types.types import User, UserRecord, UserGroup, UserMapping
from user_groups import UserGroups
from bson.objectid import ObjectId

USERS_CATEGORY_NAME = 'users'

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class Users():
    def __init__(self, instance):
        self.instance = instance

#----------------------------------------------------------------------------------------------
    def init(self):
        self.cat = self.instance.connection.db[USERS_CATEGORY_NAME]

#----------------------------------------------------------------------------------------------
    def addUser(self, user_spec, group, rights):
        '''add new user. if group_id = None create new user group with user admin rights 
           otherwise group_id and rights should be set
           @return boolean value True if success otherwise False'''
        
        UNIQUE_FIELD_NAME = 'email'
        
        out = False
        if not self.get_user_by_name(user_spec[UNIQUE_FIELD_NAME]):
            if group:
                group = self.instance.user_groups.get_user_group(group._id)
                if group:
                    user_id = str(ObjectId())
                    
                    user_spec['_id'] = user_id
                    user_spec['group_id'] = group._id
                    
                    new_user = User(user_spec)
                    self.cat.insert(new_user.get())
                    
                    group.addUserRecord(new_user._id, rights)
                    
                    self.instance.user_settings.createUserSettings(new_user)
                    self.instance.user_groups.update_user_group(group)
                    
                    out = True
                else:
                    print('[Users::addUser] failed get group %s'%str(group_id))
            else: # no specified group_id, create group and assign user to it
                
                new_group = self.instance.user_groups.createUserGroup()
                
                user_spec['_id'] = str(ObjectId())
                user_spec['group_id'] = new_group._id
                
                new_user = User(user_spec) # TODO check spec valid?
                
                self.instance.user_settings.createUserSettings(new_user)
                self.instance.user_groups.moveUser(new_user, new_group, rights)
                
                self.cat.insert(new_user.get())
                out = True
        else:
            print('[Users::addUser] user {} already exist'.format(user_spec['email']))
            
        return out

#----------------------------------------------------------------------------------------------
    def removeUserById(self, user_id):
        out = False
        user = self.getUserById(user_id)
        if user:
            out = self.removeUser(user)
        return out
       
#----------------------------------------------------------------------------------------------
    def removeUser(self, user_object, clear_all_if_empty_group = False):
        ''' removes user by id. cause modifying user group and remove it if necessary'''
        out = False
        
        user = self.getUserById(user_object._id)
        if user:
            group = self.instance.user_groups.get_user_group(user.group_id)
            if group:
                self.instance.user_groups.removeUserFromGroup(user, group)
                
                user_settings = self.instance.user_settings.getUserSettings(user._id)
                if user_settings:
                    self.instance.user_settings.removeUserSettings(user_settings)
                else:
                    print('failed to remove user settings')
                    
                if group.usersNum() == 0 and clear_all_if_empty_group:
                    self.instance.user_groups.removeGroup(group)
                else:
                    self.instance.user_groups.update_user_group(group)
                    
                self.cat.remove({"_id": user._id})
                out = True
            else:
                print('[Users::removeUser] invalid group')
        else:
            print("[Users::remove_user] user {} does'nt exist".format(id))
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