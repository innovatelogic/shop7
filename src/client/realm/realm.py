
from connections.ms_connection import MSConnection
from common.db.types.types import UserSettings
from router import Router

class Realm():
    def __init__(self, ms_connection, specs, connection_info):
        self.ms_connection_ = ms_connection
        self.specs = specs
        self.connection_info = connection_info
        self.user_settings = None
        self.user_settings_changed = True
        self.router = Router()
        
    def ms_connection(self):
        return self.ms_connection_
    
    def logout(self):
        self.ms_connection().send_msg('logout', {})
    
    def blocking_request(self, opcode, params, command):
        pass
    
    def get_categiries_1st_lvl(self, aspect):
        return self.ms_connection().send_msg('get_categiries_1st_lvl', {'id':1, 'aspect':aspect})['res']
    
    def get_category_childs(self, aspect, _id):
        return self.ms_connection().send_msg('get_category_childs', {'id':str(_id), 'aspect':aspect})['res']
    
    def get_user_categiries_1st_lvl(self):
        return self.ms_connection().send_msg('get_categiries_1st_lvl', {'id':1, 'aspect':''})['res']
    
    def get_user_category_childs(self, _id):
        return self.ms_connection().send_msg('get_category_childs', {'id':str(_id), 'aspect':''})['res']
    
    def get_items(self, aspect, _id, offset = 0, count = 50):
        items = self.ms_connection().send_msg('get_items', {'category_id':str(_id), 'offset':offset})
        return items
    
    def get_aspects(self):
        return self.ms_connection().send_msg('get_aspects', {})['res']

    def get_user_settings(self):
        if self.user_settings_changed:
            dict = self.ms_connection().send_msg('get_user_settings', {})['res']
            self.user_settings = UserSettings(dict)
            self.user_settings_changed = False
        return self.user_settings
    
    def set_user_settings(self, settings):
        self.user_settings_changed = True
        res = self.ms_connection().send_msg('set_user_settings', {'settings':settings.get()})['res']
        self.get_user_settings()
        
    def get_category_info(self, aspect, category_id):
        return self.ms_connection().send_msg('get_category_info', {'category_id':str(category_id), 'aspect':aspect})['res']