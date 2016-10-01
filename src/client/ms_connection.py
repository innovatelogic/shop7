import pika
import threading
import uuid

class MSConnection(threading.Thread):
    def __init__(self, specs, *args, **kwargs):
        super(MSConnection, self).__init__(*args, **kwargs)
        self.specs = specs
        self.connection = None
        self.channel = None
    
    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port = 5672))
        
        self.channel = self.connection.channel()
        
        #self.channel.queue_declare(queue=self.specs['ms_server']['queue'])
        
        self.result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = self.result.method.queue

        self.channel.basic_consume(self.on_response, queue='ms-client-pipe-XCXX', no_ack=True)
        pass
    
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
        
    def send(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(exchange='',
                      routing_key='ms-client-pipe-XCXX',
                       properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                      body=body)
        
        while self.response is None:
            self.connection.process_data_events()
        
        return self.response
    
    
    def stop(self):
        pass
    