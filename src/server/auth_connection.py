import pika

AUTH_MS_CHANNEL_NAME = 'ms-auth-pipe'

class AuthConnection:
    '''process communication between master server & auth'''
    def __init__(self, master, specs):
        self.master = master
        self.specs = specs
        pass
        
    def start(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.specs['master']['host']))
        
        channel = connection.channel()
        
        channel.queue_declare(queue=AUTH_MS_CHANNEL_NAME)
        
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(self.callback,
                              queue=AUTH_MS_CHANNEL_NAME,
                              no_ack=True)
        
        print('auth channel consuming: STARTED')
        
        channel.start_consuming()
    
    def stop(self):
        pass
    
    def callback(self, ch, method, props, body):
        
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
