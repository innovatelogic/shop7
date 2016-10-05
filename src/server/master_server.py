import sys
import time
from pika.connection import ConnectionParameters
from twisted.internet import protocol, reactor
from pika.adapters.twisted_connection import TwistedProtocolConnection
from bson.objectid import ObjectId

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

#----------------------------------------------------------------------------------------------
    def authentificateUser(self, login, password):
        loginPass = False
        ausPass = False
        print 'find_one'
        user = self.db_connection.db['users'].find_one({'email':login})
        print 'find_one pass'
        #check password
        if user['password'] == password:
            loginPass = True
        
        user_session = None
        
        #check already not authentificated
        if loginPass == True:
            user_session = None #self.userSessions.get(user['_id'])
            
            _id = user['_id']
            for key, session in self.userSessions.iteritems():
                if session.id == _id:
                    user_session = session
                    break
            
            if user_session == None:
                user_session = UserSession(++USER_TOKEN_START, user['_id'], user['nick'])
                self.userSessions[user_session.token] = user_session
                ausPass = True
            else:
                print(time.asctime(), "user try to %s re-authentificate" % login)
                ausPass = True
                    
            print(time.asctime(), "user %s authentificate OK" % login)
        else:
            print(time.asctime(), "user %s authentificate FAILED" % login)
        
        return [loginPass and ausPass, user_session]

#----------------------------------------------------------------------------------------------
    def activateUserAuth(self, token):
        out = False
        user_session = self.userSessions[token]
        
        if user_session:
            if not user_session.activated:
                user_session.activated = True
                out = True 
        print(time.asctime(), "user {0} activated {1}".format(user_session.name, str(out)))
        return out

#----------------------------------------------------------------------------------------------
    def logoutUser(self, token):
        out = False
        name = str(token)
        user_session = self.userSessions.get(token)
        if user_session:
            name = user_session.name
            del self.userSessions[token]
            out = True
        print(time.asctime(), "user {0} logout {1}".format(name, str(out)))
        return out
    
#----------------------------------------------------------------------------------------------    
    def get_groups(self, str_id):
        
        out = []
        if str_id == '-1':
            root = self.db_connection.db['item_groups'].find_one({'parent_id': None})
            if root:
                out.append({'id':str(root['_id']), 'parent_id': None, 'name':root['name']})
        elif str_id == '-2':
            out = self.get_groups('-1')
            groups = self.db_connection.db['item_groups'].find({'parent_id': ObjectId(out[0]['id'])})
            for group in groups:
                 out.append({'id':str(group['_id']), 'parent_id': str(group['parent_id']), 'name':group['name']})
        else:
            groups = self.db_connection.db['item_groups'].find({'parent_id': ObjectId(str_id)})
            for group in groups:
                 out.append({'id':str(group['_id']), 'parent_id': str(group['parent_id']), 'name':group['name']})
                
        return out