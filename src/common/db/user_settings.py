from types.types import UserSettings
from bson.objectid import ObjectId

USER_SETTINGS_CATEGORY_NAME = 'user_settings'

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class UserSettingsDB():
    def __init__(self, instance):
        self.instance = instance

#----------------------------------------------------------------------------------------------
    def init(self):
        self.cat = self.instance.connection.db[USER_SETTINGS_CATEGORY_NAME]

#----------------------------------------------------------------------------------------------
    def getUserSettings(self, user_id):
        '''retrieve data from db.
         @return constructed UserSettings object'''
        data = self.cat.find_one({'user_id':user_id})
        if data:
            data['_id'] = str(data['_id'])
            return UserSettings(data)
        return None

#----------------------------------------------------------------------------------------------
    def add_settings(self, settings):
        self.cat.insert(settings.get())

#----------------------------------------------------------------------------------------------
    def removeUserSettings(self, settings):
        '''
        @param settings: UserSettings object
        @return True if removed otherwise False 
         '''
        out = False
        if settings:
            self.cat.remove({"_id":settings._id})
            out = True
        return out
        
#----------------------------------------------------------------------------------------------
    def update_user_settings(self, settings):
        self.cat.update_one({'user_id':settings.user_id}, {'$set': {'options' : settings.options}})
        
#----------------------------------------------------------------------------------------------
    def createUserSettings(self, user):
        out = False
        if user and self.getUserSettings(user._id) == None:
            self.add_settings(UserSettings({'_id':ObjectId(), 'user_id':user._id}))
            out = True
        return out

#----------------------------------------------------------------------------------------------
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()        