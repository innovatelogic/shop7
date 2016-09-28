import sys
import time
from user_session import UserSession
from auth_connection import AuthConnection
import common.connection_db

USER_TOKEN_START = 456890

class MasterServer:
    def __init__(self, specs):
        self.specs = specs
        self.auth_handler = AuthConnection(self,specs)
        self.db_connection = None
        self.userSessions = {}
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
        ausPass = False
        
        users = self.db_connection.db['users'].find({'email':login})
        
        #check password
        for user in users:
            if user['password'] == password:
                loginPass = True
            break
        
        user_session = None
        
        #check already not authentificated
        if loginPass == True:
            if self.userSessions.get(user['_id']) == None:
                user_session = UserSession(++USER_TOKEN_START, user['_id'], user['nick'])
                self.userSessions[user['_id']] = user_session
                ausPass = True
            else:
                print(time.asctime(), "user try to %s re-authentificate" % login)
                    
            print(time.asctime(), "user %s authentificate OK" % login)
        else:
            print(time.asctime(), "user %s authentificate FAILED" % login)
        
        return [loginPass and ausPass, user_session]
    
    