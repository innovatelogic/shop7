
class MSConnection():
    def __init__(self, specs):
        self.specs = specs
        self.connection = None
        self.channel = None
        pass
    
    def start(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.specs['ms_server']['host']))
        
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue=self.specs['ms_server']['queue'])
        
        self.result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = self.result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
        pass
    
    
    def stop(self):
        pass
    