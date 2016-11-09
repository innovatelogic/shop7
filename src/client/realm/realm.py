
from connections.ms_connection import MSConnection
from router import Router

class Realm():
    def __init__(self, ms_connection, specs, connection_info):
        self.ms_connection_ = ms_connection
        self.specs = specs
        self.connection_info = connection_info
    
        self.router = Router()
        
    def ms_connection(self):
        return self.ms_connection_
    
    def blocking_request(self, opcode, params, command):
        pass
    
    def get_categiries_1st_lvl(self, aspect):
        result = self.ms_connection().send_msg('get_groups', {'id':1})
        return result['res']
    
    def get_category_childs(self, aspect, _id):
        result = self.ms_connection().send_msg('get_category_childs', {'id':str(_id)})
        return result['res']
    
    def get_items(self, aspect, _id, offset = 0, count = 50):
        items = self.ms_connection().send_msg('get_items', {'category_id':str(_id), 'offset':offset})
        return items
    
    def get_aspects(self):
        result = self.ms_connection().send_msg('get_aspects', {})
        return result['res']