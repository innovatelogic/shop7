import pika

AUTH_MS_CHANNEL_NAME = 'ms-auth-pipe'

class MSConnection:
    def __init__(self, specs):
        self.specs = specs
        self.connection = None
        self.channel = None
        pass
        
    def start(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.specs['auth_server']['host']))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=AUTH_MS_CHANNEL_NAME)

    def stop(self):
        self.connection.close()
        
    def send(self, body):
        self.channel.basic_publish(exchange='',
                      routing_key=AUTH_MS_CHANNEL_NAME,
                      body=body)
    
