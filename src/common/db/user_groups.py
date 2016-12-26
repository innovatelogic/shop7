from types.types import UserGroup, UserRecord
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
            if last user removed from group all subsequent records will be removed
            @param user to add
            @param group to add
            @return: True if operation success otherwise False
        '''
        out = False
        if user and group:
            if group._id != user.group_id:
                self.remove_user_from_group(group._id, user._id)
        
            group.addUserRecord(user._id, rights)
            out = True
        return out

#----------------------------------------------------------------------------------------------
    def removeUserFromGroup(self, user, group):
        group = self.get_user_group(user.group_id)
        if group and user:
            self.remove_user_from_group(group._id, user._id)
        pass

#----------------------------------------------------------------------------------------------       
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()