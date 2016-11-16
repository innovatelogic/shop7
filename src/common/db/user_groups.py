from types.types import UserGroup, UserRecord
from bson.objectid import ObjectId

USER_GROUPS_CATEGORY_NAME = 'user_groups'

class UserGroups():
    def __init__(self, instance):
        self.instance = instance
        
    def init(self):
        self.cat = self.instance.connection.db[USER_GROUPS_CATEGORY_NAME]
    
    def add_user_group(self, group):
        self.cat.insert(group.get())
    
    def get_user_group(self, id):
        '''retrieve data from db. form spec and constructs UserGroup object'''
        data = self.cat.find_one({'_id':id})
        if data:
            spec = {'_id': str(data['_id']), 'aspect_id':str(data['aspect_id'])}
            spec['records'] = []
            for key, value in data['records'].iteritems():
                spec['records'].append(UserRecord(key, value))
            return UserGroup(spec)
        return None
    
    def remove_user_from_group(self, group_id, user_id):
        '''remove user from group and delete group if no users left'''
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
    
    def remove_group(self, group_id):
        self.cat.remove({"_id":group_id})
        
    def update_user_group(self, group):
        self.cat.update_one({
          '_id': group._id
        },{
          '$set': {
            'records': group.records
          }
        }, upsert=False)
        
    def get_all_groups(self):
        ''' retreieve all user groups'''
        data = self.cat.find({})
        items = []
        for i in data:
            spec = {'_id': str(i['_id']), 'aspect_id':str(i['aspect_id'])}
            spec['records'] = []
            for key, value in i['records'].iteritems():
                spec['records'].append(UserRecord(key, value))
            items.append(UserGroup(spec))
        return items
        
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()