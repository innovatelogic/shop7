import os, sys, time
import subprocess
from pika.connection import ConnectionParameters
from twisted.internet import protocol, reactor
from pika.adapters.twisted_connection import TwistedProtocolConnection
from common.models.realm import Realm

from connections.auth_connection import AuthConnection
from connections.client_connection import ClientsConnection
from common.utils import log

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class MasterServer:
    def __init__(self, specs):
        self.specs = specs
        self.auth_handler = None
        self.clients_connection = None
        self.__realm = Realm(self.specs)
        pass
    
#----------------------------------------------------------------------------------------------
    def run(self):
        log.MsgOK("Master Server Starts")
        
        parameters = ConnectionParameters(heartbeat_interval=0)
        
        cc = protocol.ClientCreator(reactor,
                                    TwistedProtocolConnection,
                                    parameters)
        
        self.auth_handler = AuthConnection(self, self.specs, cc)
        self.clients_connection = ClientsConnection(self, self.specs, cc)
        
        self.__realm.start()
        
        self.auth_handler.start()
        self.clients_connection.start()
        
        #self.start_auth_server()
        
        reactor.run()

        self.__realm.stop()
        
        log.Msg("Master Server Stops")
        
#----------------------------------------------------------------------------------------------
    def realm(self):
        return self.__realm

#----------------------------------------------------------------------------------------------
    def start_auth_server(self):
        subprocess.Popen(self.specs['path']['auth_proc'], shell=True)
        