import pika

from twisted.internet import defer, protocol, task

class AuthConnection:
    '''process communication between master server & auth'''
    def __init__(self, master, specs, client_creator):
        self.master = master
        self.specs = specs
        self.client_creator = client_creator
        
    @defer.inlineCallbacks
    def run(self, connection):
        
        channel = yield connection.channel()
    
        exchange = yield channel.exchange_declare(exchange='topic_link', type='topic')
    
        queue = yield channel.queue_declare(queue=self.specs['master']['ms_auth_queue'], auto_delete=False, exclusive=False)
    
        yield channel.queue_bind(exchange='topic_link', queue=self.specs['master']['ms_auth_queue'])
    
        yield channel.basic_qos(prefetch_count=1)
    
        queue_object, consumer_tag = yield channel.basic_consume(queue=self.specs['master']['ms_auth_queue'], no_ack=True)
    
        l = task.LoopingCall(self.read, queue_object)
    
        l.start(0.01)
        
        print('Auth connection queue established')
        
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
            self.do_auth(ch, method, properties, body)
    
        #yield ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def do_auth(self, ch, method, props, body):
        
        dict = eval(body)
        flag, user = self.master.authentificateUser(dict['login'], dict['password'])
        
        reply = ''
        if flag and user:
            reply = str({'auth':flag, 'token':user.token, 'name':user.name})
        
        ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(reply))
        
        #ch.basic_ack(delivery_tag = method.delivery_tag)
