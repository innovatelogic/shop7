
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
    
    