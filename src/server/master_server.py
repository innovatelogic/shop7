import sys, time
from pika.connection import ConnectionParameters
from twisted.internet import protocol, reactor
from pika.adapters.twisted_connection import TwistedProtocolConnection
from bson.objectid import ObjectId
from models.category_model import CategoryModel
from models.users_model import UsersModel
from models.items_cache_model import ItemsCacheModel
from models.base_aspects_container import BaseAspectsContainer
from models.user_aspects_container import UserAspectsContainer

from connections.auth_connection import AuthConnection
from connections.client_connection import ClientsConnection

import common.db.instance
    
#----------------------------------------------------------------------------------------------
class MasterServer:
    def __init__(self, specs):
        self.specs = specs
        self.auth_handler = None
        self.clients_connection = None
        self.db = common.db.instance.Instance(self.specs)
        self.category_model = CategoryModel(self.db)
        self.users_model = UsersModel(self.db)
        self.items_cache_model = ItemsCacheModel(self.db)
        self.base_aspects_container = BaseAspectsContainer(self.db)
        self.user_aspects_container = UserAspectsContainer(self.db)
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
        
        self.load()
        
        self.auth_handler.start()
        self.clients_connection.start()

        reactor.run()

        self.db.disconnect()
        
        print(time.asctime(), "Master Server Stops")
    
    def load(self):
        self.base_aspects_container.load()
        #self.category_model.load()
        