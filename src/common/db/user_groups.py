from types.types import UserGroup, UserRecord

USER_GROUPS_CATEGORY_NAME = 'user_groups'

class UserGroups():
    def __init__(self, instance):
        self.instance = instance
        
    def init(self):
        self.cat = self.instance.connection.db[USER_GROUPS_CATEGORY_NAME]
    
    def add_user_group(self, group):
        self.cat.insert(group.get())
    
    def get_user_group(self, id):
        print('get_user_group')
        data = self.cat.find_one({'_id':id})
        if data:
            spec = {'_id': str(data['_id'])}
            spec['records'] = []
            for key, value in data['records'].iteritems():
                spec['records'].append(UserRecord(key, value))
            return UserGroup(spec)
        return None
    
    def update_user_group(self, group):
        self.cat.update_one({
          '_id': group._id
        },{
          '$set': {
            'records': group.records
          }
        }, upsert=False)
    
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()