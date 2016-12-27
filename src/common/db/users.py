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
                
                user_id = str(ObjectId())
                group_id = str(ObjectId())
                user_mapping_id = str(ObjectId())
                
                user_spec['_id'] = user_id
                user_spec['group_id'] = group_id

                mapping_spec = {}
                mapping_spec['_id'] = user_mapping_id
                mapping_spec['group_id'] = group_id
                mapping_spec['mapping'] = []
                
                spec_group = {'_id':group_id, 'user_mapping_id':user_mapping_id}          
                spec_group['records'] = []
                spec_group['records'].append(UserRecord(user_spec['_id'], rights))
                
                userAspect = self.instance.user_aspects.createUserAspect(group_id)
                spec_group['aspect_id'] = userAspect._id
                
                new_group = UserGroup(spec_group)
                new_user = User(user_spec) # TODO check spec valid?
                new_mapping = UserMapping(mapping_spec)
                
                self.instance.user_settings.createUserSettings(new_user)
                self.instance.user_groups.add_user_group(new_group)
                self.instance.group_category_mapping.addMapping(new_mapping)
                self.cat.insert(new_user.get())
                
                out = True
        else:
            print('[Users::addUser] user {} already exist'.format(user_spec['email']))
            
        return out

#----------------------------------------------------------------------------------------------
    def removeUser(self, id):
        ''' removes user by id. cause modifying user group and remove it if necessary'''
        out = False
        data = self.cat.find_one({'_id':id})
        
        if data:
            res = self.instance.user_groups.remove_user_from_group(data['group_id'], data['_id'])
            self.cat.remove({"_id": data['_id']})
            out = True
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