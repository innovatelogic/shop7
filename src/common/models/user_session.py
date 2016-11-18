from common.db.types.types import UserSettings

class UserSession:
    def __init__(self, token, id, name, group_id):
        ''' creates when auth ok'''
        self.activated = False
        self.time_started = ''
        self.token = token
        self.id = id
        self.name = name
        self.group_id = group_id
        self.settings = UserSettings({'active_base_aspect':'prom_ua', 'show_base_aspect_whole_tree':True})
        pass
    
    #-----------------------------------------------------------------------------------------
    def start(self):
        ''' statrs when user connected to master server'''
        pass
    
    #----------------------------------------------------------------------------------------------    
    def close(self):
        ''' ends when user disconnect from master server'''
        pass