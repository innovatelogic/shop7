import pika

AUTH_MS_CHANNEL_NAME = 'ms-auth-pipe'

class AuthConnection:
    def __init__(self, specs):
        self.specs = specs
        pass
        
    def start(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.specs['master']['host']))
        
        channel = connection.channel()
        
        channel.queue_declare(queue=AUTH_MS_CHANNEL_NAME)
        
        channel.basic_consume(self.callback,
                              queue=AUTH_MS_CHANNEL_NAME,
                              no_ack=True)
        
        print('master server auth channel: STARTED')
        
        channel.start_consuming()
        pass
    
    def stop(self):
        pass
    
    def callback(self, ch, method, properties, body):
            print(" [x] Received %r" % body)