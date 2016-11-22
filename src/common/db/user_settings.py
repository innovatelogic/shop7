from types.types import UserSettings

USER_SETTINGS_CATEGORY_NAME = 'user_settings'

class UserSettingsDB():
    def __init__(self, instance):
        self.instance = instance

#----------------------------------------------------------------------------------------------        
    def init(self):
        self.cat = self.instance.connection.db[USER_SETTINGS_CATEGORY_NAME]

#----------------------------------------------------------------------------------------------        
    def get_user_settings(self, user_id):
        '''retrieve data from db. return constructed UserSettings object'''
        data = self.cat.find_one({'user_id':user_id})
        if data:
            data['_id'] = str(data['_id'])
            return UserSettings(data)
        return None

#----------------------------------------------------------------------------------------------        
    def add_settings(self, settings):
        self.cat.insert(settings.get())
        
#----------------------------------------------------------------------------------------------        
    def update_user_settings(self, settings):
        self.cat.update_one({'user_id':settings.user_id}, {'$set': {'options' : settings.options}})

#----------------------------------------------------------------------------------------------       
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()        