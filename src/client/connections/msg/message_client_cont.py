import importlib
from messages import Message
import xml.etree.ElementTree

#----------------------------------------------------------------------------------------------
class MessageClientContaier():
    def __init__(self, connection_info, channel, callback_queue, filename):
        self.connection_info = connection_info
        self.channel = channel
        self.callback_queue = callback_queue
        self.filename = filename
        self.dict_messages = {}
        self.__load(self.filename)
    
    def __load(self, filename):
        e = xml.etree.ElementTree.parse(filename).getroot()
        
        for msg in e.findall('msg'):
            msg_name = msg.get('name')
            for clt in msg.findall('client'):
                class_ = getattr(importlib.import_module("connections.msg.messages"), 'Message_client_' + msg_name)
                self.dict_messages[msg_name] = class_(self.connection_info, self.channel, self.callback_queue, clt.get('get'), clt.get('send'))
                break
                
    def send_msg(self, name, params, corr_id):
        self.dict_messages[name].send(params, corr_id)   