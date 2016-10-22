import pika
import threading
import uuid
#from pika.credentials import ExternalCredentials
from msg.message_client_cont import MessageClientContaier

class MSConnection(threading.Thread):
    ''' establish connection with MS'''
    ''' connection info format
        reply = {'auth':flag,
                  'token':user.token,
                  'name':user.name,
                  'ms_host':self.specs['master']['host'],
                  'queue':self.specs['master']['ms_client_queue'],
                  'queue_port':self.specs['master']['ms_queue_port']}
'''

    def __init__(self, connection_info, ready=None, *args, **kwargs):
        super(MSConnection, self).__init__(*args, **kwargs)
        self.ready = ready
        self.connection_info = connection_info
        self.connection = None
        self.channel = None
        
    
    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.connection_info['ms_host'],
                                                                             port=int(self.connection_info['queue_port'])
                                                                             ))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.connection_info['queue'], auto_delete=True)
        self.result = self.channel.queue_declare()
        self.callback_queue = self.result.method.queue
        self.queue_name = self.result.method.queue
        #print self.result.method.queueame
        
        self.msg_client_cont = MessageClientContaier(self.connection_info, self.channel, self.callback_queue, '../res/msg/messages.xml')

        self.channel.basic_consume(self.on_response, queue=self.queue_name, no_ack=True)
        self.ready.set()
    
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
    def send_msg(self, name, params):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        
        self.msg_client_cont.send_msg(name, params, self.corr_id)
        
        while self.response is None:
            self.connection.process_data_events()
            
        return eval(self.response)
    
    def stop(self):
        self.connection.close()
        pass
    