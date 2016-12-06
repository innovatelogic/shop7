import pika

from twisted.internet import defer, protocol, task
from common.msg.message_cont import MessageContaier, EAspect

class ClientsConnection:
    '''process communication between clients & ms'''
    def __init__(self, master, specs, client_creator):
        self.master = master
        self.specs = specs
        self.client_creator = client_creator
        self.message_cont = MessageContaier(self.master, '../res/msg/messages.xml', EAspect.EAspect_Server)
        
    #----------------------------------------------------------------------------------------------
    @defer.inlineCallbacks
    def run(self, connection):
        
        channel = yield connection.channel()
        
        exchange = yield channel.exchange_declare(exchange='1', type='topic')
    
        queue = yield channel.queue_declare(queue=self.specs['master']['ms_client_queue'], auto_delete=True, exclusive=False)
    
        yield channel.queue_bind(exchange='1', queue=self.specs['master']['ms_client_queue'])
    
        yield channel.basic_qos(prefetch_count=1)
    
        queue_object, consumer_tag = yield channel.basic_consume(queue=self.specs['master']['ms_client_queue'], no_ack=True)
    
        l = task.LoopingCall(self.read, queue_object)
    
        l.start(0.01)
        
        print('Clients connection queue established')
    
    #----------------------------------------------------------------------------------------------
    def start(self):
        d = self.client_creator.connectTCP(self.specs['master']['host'], self.specs['master']['ms_queue_port'])
        d.addCallback(lambda protocol: protocol.ready)
        d.addCallback(self.run)
    
    #----------------------------------------------------------------------------------------------    
    def stop(self):
        pass
    
    #----------------------------------------------------------------------------------------------
    @defer.inlineCallbacks
    def read(self, queue_object):
        ch, method, properties, body = yield queue_object.get()
    
        if body:
            self.process_msg(ch, method, properties, body)
    
        #yield ch.basic_ack(delivery_tag=method.delivery_tag)
    
    #----------------------------------------------------------------------------------------------    
    def process_msg(self, ch, method, properties, body):
        self.message_cont.process_msg(ch, method, properties, body)
        
