
from connections.ms_connection import MSConnection
from common.db.types.types import UserSettings
from router import Router
from items_category_state import ItemsCategoryState
from connections.msg.messages import Message_client_get_category_info
from connections.msg.messages import Message_client_logout
from connections.msg.messages import Message_client_get_categiries_1st_lvl
from connections.msg.messages import Message_client_get_category_childs
from connections.msg.messages import Message_client_get_items
from connections.msg.messages import Message_client_get_aspects
from connections.msg.messages import Message_client_get_user_settings
from connections.msg.messages import Message_client_set_user_settings
from connections.msg.messages import Message_client_get_user_category_info

class Realm():
    def __init__(self, ms_connection, specs, connection_info):
        self.ms_connection_ = ms_connection
        self.specs = specs
        self.connection_info = connection_info
        self.user_settings = None
        self.user_settings_changed = True
        self.items_category_state = ItemsCategoryState()

#----------------------------------------------------------------------------------------------        
    def ms_connection(self):
        return self.ms_connection_

#----------------------------------------------------------------------------------------------
    def logout(self):
        self.ms_connection().send_msg(Message_client_logout.opcode(), {})

#----------------------------------------------------------------------------------------------
    def blocking_request(self, opcode, params, command):
        pass
    
#----------------------------------------------------------------------------------------------
    def get_categiries_1st_lvl(self, aspect):
        return self.ms_connection().send_msg(Message_client_get_categiries_1st_lvl.opcode(),
                                              {'id':1, 'aspect':aspect})['res']

#----------------------------------------------------------------------------------------------
    def get_category_childs(self, aspect, _id):
        return self.ms_connection().send_msg(Message_client_get_category_childs.opcode(), 
                                             {'id':str(_id), 'aspect':aspect})['res']
    
#----------------------------------------------------------------------------------------------
    def get_user_categiries_1st_lvl(self):
        return self.ms_connection().send_msg(Message_client_get_categiries_1st_lvl.opcode(),
                                              {'id':1, 'aspect':''})['res']

#----------------------------------------------------------------------------------------------
    def get_user_category_childs(self, _id):
        return self.ms_connection().send_msg(Message_client_get_category_childs.opcode(), 
                                             {'id':str(_id), 'aspect':''})['res']

#----------------------------------------------------------------------------------------------
    def get_items(self, aspect, category_id, offset = 0, count = 50):
        items = self.ms_connection().send_msg(Message_client_get_items.opcode(),
                                               {'aspect':aspect, 'category_id':str(category_id), 'offset':offset, 'count':count})
        return items
    
#----------------------------------------------------------------------------------------------
    def get_user_category_items(self, category_id, offset = 0, count = 50):
        items = self.ms_connection().send_msg(Message_client_get_user_category_items.opcode(),
                                               {'category_id':str(category_id), 'offset':offset, 'count':count})
        return items
        
#----------------------------------------------------------------------------------------------
    def get_aspects(self):
        return self.ms_connection().send_msg(Message_client_get_aspects.opcode(), {})['res']

#----------------------------------------------------------------------------------------------
    def get_user_settings(self):
        if self.user_settings_changed:
            dict = self.ms_connection().send_msg(Message_client_get_user_settings.opcode(), {})['res']
            self.user_settings = UserSettings(dict)
            self.user_settings_changed = False
        return self.user_settings

#----------------------------------------------------------------------------------------------
    def set_user_settings(self, settings):
        self.user_settings_changed = True
        res = self.ms_connection().send_msg(Message_client_set_user_settings.opcode(),
                                            {'settings':settings.get()})['res']
        self.get_user_settings()

#----------------------------------------------------------------------------------------------
    def get_category_info(self, aspect, category_id):
        return self.ms_connection().send_msg(Message_client_get_category_info.opcode(), 
                                             {'category_id':str(category_id), 'aspect':aspect})['res']

#----------------------------------------------------------------------------------------------
    def get_user_category_info(self, category_id):
        return self.ms_connection().send_msg(Message_client_get_user_category_info.opcode(), 
                                             {'category_id':str(category_id)})['res']
                                             
#----------------------------------------------------------------------------------------------
    def set_items_category_state(self, aspect, category_id, count, offset):
        self.items_category_state.set(aspect, category_id, count, offset)

#----------------------------------------------------------------------------------------------
    def get_items_category_state(self):
        return self.items_category_state