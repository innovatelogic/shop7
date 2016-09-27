import sys
import time
from user_session import UserSession
from auth_connection import AuthConnection

class MasterServer:
    def __init__(self, specs):
        self.auth_handler = AuthConnection(self,specs)
        pass
    
    def run(self):
        
        print(time.asctime(), "Master Server Starts")
        
        self.auth_handler.start()
        
        print(time.asctime(), "Master Server Stops")
    
    def authentificateUser(self, login, password):
        print login
        print password
        
        pass
    