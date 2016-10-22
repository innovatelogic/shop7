import importlib
from message import Message
import xml.etree.ElementTree

class EAspect:
    EAspect_Client = 0
    EAspect_Server = 1
    EAspect_MAX    = 2

#----------------------------------------------------------------------------------------------
class MessageContaier():
    def __init__(self, master, filename, aspect):
        self.master = master
        self.aspect = aspect
        self.filename = filename
        self.dict_messages = {}
        self.__load(self.filename)
    
    def __load(self, filename):
        e = xml.etree.ElementTree.parse(filename).getroot()
        
        for msg in e.findall('msg'):
            msg_name = msg.get('name')
            class_ = getattr(importlib.import_module("common.msg.message"), 'Message_server_' + msg_name)
            if self.aspect == EAspect.EAspect_Client:
                for clt in msg.findall('client'):
                    self.dict_messages[msg_name] = class_(self.master, clt.get('get'), clt.get('send'))
                    break
            elif self.aspect == EAspect.EAspect_Server:
                for srv in msg.findall('server'):
                    self.dict_messages[msg_name] = class_(self.master, srv.get('get'), srv.get('send'))
                    break
                
    def process_msg(self, ch, method, props, body):
        dict = eval(body)
        self.dict_messages[dict['opcode']].process(ch, method, props, body)     