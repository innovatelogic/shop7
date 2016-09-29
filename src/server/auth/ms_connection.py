import pika
import uuid

class MSConnection:
    def __init__(self, specs):
        self.specs = specs
        self.connection = None
        self.channel = None
        pass
        
    def start(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.specs['ms']['host']))
        
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue=self.specs['ms']['ms_auth_queue'])
        
        self.result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = self.result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)


    def stop(self):
        self.connection.close()
        
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
        
    def send(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(exchange='',
                      routing_key=self.specs['ms']['ms_auth_queue'],
                       properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                      body=body)
        
        while self.response is None:
            self.connection.process_data_events()
        
        return self.response