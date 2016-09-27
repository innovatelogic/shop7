import sys
import time
from user_session import UserSession
from auth_connection import AuthConnection
import common.connection_db

class MasterServer:
    def __init__(self, specs):
        self.specs = specs
        self.auth_handler = AuthConnection(self,specs)
        self.db_connection = None
        pass
    
    def run(self):
        
        print(time.asctime(), "Master Server Starts")
        
        self.connectDB()
        
        self.auth_handler.start()
        
        self.disconnectDB()
        
        print(time.asctime(), "Master Server Stops")
        
    def connectDB(self):
        self.db_connection = common.connection_db.ConnectionDB(self.specs)
        self.db_connection.connect()
        
    def disconnectDB(self):
        self.db_connection.close()
    
    def authentificateUser(self, login, password):
        loginPass = False
        
        users = self.db_connection.db['users'].find({'email':login})
        
        for user in users:
            if user['password'] == password:
                loginPass = True
            break
        
        if loginPass:
            print("user %s authentificate OK" % login)
        else:
            print("user %s authentificate FAILED" % login)
        
        return loginPass
    