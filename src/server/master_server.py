import sys
import time
from pika.connection import ConnectionParameters
from twisted.internet import protocol, reactor
from pika.adapters.twisted_connection import TwistedProtocolConnection

from user_session import UserSession
from connections.auth_connection import AuthConnection
from connections.client_connection import ClientsConnection
import common.connection_db

USER_TOKEN_START = 456890
    
#############################################################################
class MasterServer:
    def __init__(self, specs):
        self.specs = specs
        self.auth_handler = None
        self.clients_connection = None
        self.db_connection = None
        self.userSessions = {}
        pass
    
    def run(self):
        
        print(time.asctime(), "Master Server Starts")
        
        parameters = ConnectionParameters()
        cc = protocol.ClientCreator(reactor,
                                    TwistedProtocolConnection,
                                    parameters)
        
        self.auth_handler = AuthConnection(self, self.specs, cc)
        self.clients_connection = ClientsConnection(self, self.specs, cc)
        
        self.connectDB()
        
        self.auth_handler.start()
        self.clients_connection.start()

        reactor.run()

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
            user_session = self.userSessions.get(user['_id'])
            if user_session == None:
                user_session = UserSession(++USER_TOKEN_START, user['_id'], user['nick'])
                self.userSessions[user['_id']] = user_session
                ausPass = True
            else:
                print(time.asctime(), "user try to %s re-authentificate" % login)
                ausPass = True
                    
            print(time.asctime(), "user %s authentificate OK" % login)
        else:
            print(time.asctime(), "user %s authentificate FAILED" % login)
        
        return [loginPass and ausPass, user_session]
    
    def activateUserAuth(self, token):
        return True