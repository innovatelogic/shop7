import importlib
from messages import Message
import xml.etree.ElementTree

#----------------------------------------------------------------------------------------------
class MessageClientContaier():
    def __init__(self, filename):
        self.filename = filename
        self.dict_messages = {}
        self.__load(self.filename)
    
    def __load(self, filename):
        e = xml.etree.ElementTree.parse(filename).getroot()
        
        for msg in e.findall('msg'):
            msg_name = msg.get('name')
            for clt in msg.findall('client'):
                class_ = getattr(importlib.import_module("connections.msg.messages"), 'Message_client_' + msg_name)
                self.dict_messages[msg_name] = class_(clt.get('get'), clt.get('send'))
                break
                
    def send_msg(self, ch, method, props, body):
        pass     