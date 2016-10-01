import pika
import threading
import uuid

class MSConnection(threading.Thread):
    def __init__(self, specs, ready=None, *args, **kwargs):
        super(MSConnection, self).__init__(*args, **kwargs)
        self.ready = ready
        self.specs = specs
        self.connection = None
        self.channel = None
    
    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port = 5672))
        
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue='ms-client-pipe-XCXX')
        
        self.result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = self.result.method.queue

        self.channel.basic_consume(self.on_response, queue='ms-client-pipe-XCXX', no_ack=True)
        
        self.ready.set()
    
    def on_response(self, ch, method, props, body):
        print 'on_response'
        if self.corr_id == props.correlation_id:
            self.response = body
        
    def send(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        print 'send'
        self.channel.basic_publish(exchange='topic_link2',
                       routing_key='ms-client-pipe-XCXX',
                       properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                      body=body)
        
        while self.response is None:
            print 'loop'
            self.connection.process_data_events()
            
        print 'insend'
        #return self.response
        return True
    
    
    def stop(self):
        self.connection.close()
        pass
    