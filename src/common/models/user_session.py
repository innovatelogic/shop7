from bson.objectid import ObjectId
from common.db.types.user_settings import UserSettings

class UserSession:
    def __init__(self, db_instance, token, id, name, group_id):
        ''' creates when auth ok'''
        self.db_instance = db_instance
        self.activated = False
        self.time_started = ''
        self.token = token
        self.id = id
        self.name = name
        self.group_id = group_id
        self.settings = db_instance.user_settings.getUserSettings(self.id)
        pass
    
    #-----------------------------------------------------------------------------------------
    def start(self):
        ''' statrs when user connected to master server'''
        pass
    
    #----------------------------------------------------------------------------------------------    
    def close(self):
        ''' ends when user disconnect from master server'''
        pass