import pika

from twisted.internet import defer, protocol, task

class ClientsConnection:
    '''process communication between clients & ms server'''
    def __init__(self, master, specs, client_creator):
        self.master = master
        self.specs = specs
        self.client_creator = client_creator
        
    @defer.inlineCallbacks
    def run(self, connection):
        
        channel = yield connection.channel()
        
        exchange = yield channel.exchange_declare(exchange='topic_link', type='topic')
    
        queue = yield channel.queue_declare(queue=self.specs['master']['ms_client_queue'], auto_delete=False, exclusive=False)
    
        yield channel.queue_bind(exchange='topic_link', queue=self.specs['master']['ms_client_queue'])
    
        yield channel.basic_qos(prefetch_count=1)
    
        queue_object, consumer_tag = yield channel.basic_consume(queue=self.specs['master']['ms_client_queue'], no_ack=True)
    
        l = task.LoopingCall(self.read, queue_object)
    
        l.start(0.01)
        
        print('Clients connection queue established')
        
    def start(self):
        port = 5672
        d = self.client_creator.connectTCP(self.specs['master']['host'], port)
        d.addCallback(lambda protocol: protocol.ready)
        d.addCallback(self.run)
        
    def stop(self):
        pass
    
    @defer.inlineCallbacks
    def read(self, queue_object):
        ch,method,properties,body = yield queue_object.get()
    
        if body:
            print body
    
        #yield ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def callback(self, ch, method, props, body):
        print body
