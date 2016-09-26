import pika

class AuthHandler:
    def __init__(self, specs):
        self.specs = specs
        pass
        
    def start(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.specs['master']['host']))
        
        channel = connection.channel()
        
        channel.queue_declare(queue='auth-pipe')
        
        channel.basic_consume(self.callback,
                              queue='auth-pipe',
                              no_ack=True)
        
        print('master server auth channel: STARTED')
        
        channel.start_consuming()
        pass
    
    def stop(self):
        pass
    
    def callback(self, ch, method, properties, body):
            print(" [x] Received %r" % body)