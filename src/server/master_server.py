import sys

from user_session import UserSession
from auth_handler import AuthHandler

class MasterServer:
    def __init__(self, specs):
        self.auth_handler = AuthHandler(specs)
        pass
    
    
    def run(self):
        self.auth_handler.start()
        pass
    
    
    