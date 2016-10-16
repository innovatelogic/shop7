import sys, time
from pika.connection import ConnectionParameters
from twisted.internet import protocol, reactor
from pika.adapters.twisted_connection import TwistedProtocolConnection
from bson.objectid import ObjectId
from models.category_model import CategoryModel

from user_session import UserSession
from connections.auth_connection import AuthConnection
from connections.client_connection import ClientsConnection
import common.db.connection
import common.db.instance

USER_TOKEN_START = 456890
    
#----------------------------------------------------------------------------------------------
class MasterServer:
    def __init__(self, specs):
        self.specs = specs
        self.auth_handler = None
        self.clients_connection = None
        self.db = common.db.instance.Instance(self.specs)
        self.category_model = CategoryModel(self.db)
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
        
        self.db.connect()
        
        self.category_model.load()
        
        self.auth_handler.start()
        self.clients_connection.start()

        reactor.run()

        self.db.disconnect()
        
        print(time.asctime(), "Master Server Stops")
        
#----------------------------------------------------------------------------------------------
    def authentificateUser(self, login, password):
        loginPass = False
        ausPass = False
        
        print('[authentificateUser]')
        user = self.db.users.get_user_by_name(login)
        
        if user:
            print('[authentificateUser] user ok')
            if user.pwhs == password:
                loginPass = True
        
                user_session = None
                
                _id = user._id
                for key, session in self.userSessions.iteritems():
                    if session.id == _id:
                        user_session = session
                        break
                if user_session == None:
                    user_session = UserSession(++USER_TOKEN_START, user._id, user.name)
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
    
