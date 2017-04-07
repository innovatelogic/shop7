from types.user_mapping import UserMapping
from types.user_group import UserGroup
from types.user_record import UserRecord
from bson.objectid import ObjectId

USER_GROUPS_CATEGORY_NAME = 'user_groups'

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class UserGroups():
    def __init__(self, instance):
        self.instance = instance

#----------------------------------------------------------------------------------------------
    def init(self):
        self.cat = self.instance.connection.db[USER_GROUPS_CATEGORY_NAME]

#----------------------------------------------------------------------------------------------
    def add_user_group(self, group):
        self.cat.insert(group.get())

#----------------------------------------------------------------------------------------------    
    def get_user_group(self, id):
        '''retrieve data from db. form spec and constructs UserGroup object
        return UserGroup object otherwise None
        '''
        data = self.cat.find_one({'_id':id})
        if data:
            spec = {'_id': str(data['_id']), 'aspect_id':str(data['aspect_id'])}
            
            spec['user_mapping_id'] = None
            if 'user_mapping_id' in data:
                spec['user_mapping_id'] = str(data['user_mapping_id'])
            
            spec['records'] = []
            for key, value in data['records'].iteritems():
                spec['records'].append(UserRecord(key, value))
            return UserGroup(spec)
        return None

#----------------------------------------------------------------------------------------------    
    def remove_user_from_group(self, group_id, user_id):
        '''remove user from group and delete group if no users left
            return flag
        '''
        out = False
        group = self.get_user_group(group_id)
        if group:
            group.records.pop(str(user_id), None)
            if len(group.records) > 0:
                self.update_user_group(group)
            else:
                self.remove_group(group._id)
            out = True
        else:
            print("UserGroups::remove_user_from_group {} no group found".format(group_id))
        return out

#----------------------------------------------------------------------------------------------    
    def remove_group(self, group_id):
        self.cat.remove({"_id":group_id})

#----------------------------------------------------------------------------------------------
    def createUserGroup(self):
        ''' creates empty user group and store in db
        @return UserGroup object
        '''
        group_id = str(ObjectId())
        user_mapping_id = str(ObjectId())
        
        userAspect = self.instance.user_aspects.createUserAspect(group_id)
        
        mapping_spec = {}
        mapping_spec['_id'] = user_mapping_id
        mapping_spec['group_id'] = group_id
        mapping_spec['mapping'] = {}
                
        spec_group = {'_id':group_id, 'user_mapping_id':user_mapping_id, 'aspect_id':userAspect._id}          
        spec_group['records'] = []
        
        new_group = UserGroup(spec_group)
        new_mapping = UserMapping(mapping_spec)
        
        self.instance.user_groups.add_user_group(new_group)
        self.instance.group_category_mapping.addMapping(new_mapping)
        
        return new_group

#----------------------------------------------------------------------------------------------
    def removeGroup(self, group):
        out = False
        if group:
            mapping = self.instance.group_category_mapping.getMapping(group)
            if mapping:
                self.instance.group_category_mapping.removeMapping(mapping)
            else:
                print('[removeGroup] failed to get mapping')
            
            self.instance.user_aspects.removeUserAspect(group)
            
            for key, value in group.records.iteritems():
                self.instance.users.removeUserById(key)
                
            self.cat.remove({"_id":group._id})
        return out

#----------------------------------------------------------------------------------------------        
    def update_user_group(self, group):
        self.cat.update_one({
          '_id': group._id
        },{
          '$set': {
            'records': group.records
          }
        }, upsert=False)
        
#----------------------------------------------------------------------------------------------        
    def get_all_groups(self):
        ''' retreieve all user groups. return array []'''
        data = self.cat.find({})
        out = []
        for i in data:
            spec = {'_id': str(i['_id']), 'aspect_id':str(i['aspect_id'])}
            
            spec['user_mapping_id'] = None
            if 'user_mapping_id' in i:
                spec['user_mapping_id'] = str(i['user_mapping_id'])
                
            spec['records'] = []
            for key, value in i['records'].iteritems():
                spec['records'].append(UserRecord(key, value))
            out.append(UserGroup(spec))
        return out

#----------------------------------------------------------------------------------------------
    def moveUser(self, user, group, rights):
        ''' move user to group
            if user in other group remove from previous group
            save both groups
            @param user to add
            @param group to add
            @return: True if operation success otherwise False
        '''
        out = False
        if user and group:
            if user.group_id != None and group._id != user.group_id:
                prev_group = self.get_user_group(user.group_id)
                if prev_group:
                    prev_group.removeUserRecord(user._id)
                    self.update_user_group(prev_group)
        
            group.addUserRecord(user._id, rights)
            self.update_user_group(group)
            out = True
        return out

#----------------------------------------------------------------------------------------------
    def removeUserFromGroup(self, user, group):
        res = False
        if user and group:
            if group.removeUserRecord(user._id):
                self.update_user_group(group)
                res = True
        return res

#----------------------------------------------------------------------------------------------       
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()