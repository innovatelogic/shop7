import sys

from user_session import UserSession
from auth_connection import AuthConnection

class MasterServer:
    def __init__(self, specs):
        self.auth_handler = AuthConnection(specs)
        pass
    
    
    def run(self):
        self.auth_handler.start()
        pass
    
    
    