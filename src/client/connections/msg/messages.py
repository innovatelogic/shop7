import pika

class Message():
    def __init__(self, name, connection_info, channel, callback_queue, get, send):
        self.opcode = name
        self.channel = channel
        self.connection_info = connection_info
        self.callback_queue = callback_queue
        self.send_params = []
        self.get_params = []
        self.__parse(get, send)
        pass
    
    def opcode(self):
        return type(self).__name__.replace("Message_", "")

    def __parse(self, get, send):
        arr = get.split(";")
        for s in arr:
            self.get_params.append(s)
        arr = send.split(";")
        for s in arr:
            self.send_params.append(s)
            
    def send(self, params, corr_id):
        
        params['opcode'] = self.opcode
        params['token'] = self.connection_info['token']
        
        self.channel.basic_publish(exchange='',
                       routing_key=self.connection_info['queue'],
                       properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = corr_id,
                                         ),
                      body=str(params))

#----------------------------------------------------------------------------------------------
class Message_client_auth_activate(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

#----------------------------------------------------------------------------------------------
class Message_client_logout(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

#----------------------------------------------------------------------------------------------
class Message_client_get_categiries_1st_lvl(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

#----------------------------------------------------------------------------------------------
class Message_client_get_category_childs(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

#----------------------------------------------------------------------------------------------
class Message_client_get_items(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

#----------------------------------------------------------------------------------------------
class Message_client_get_aspects(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

#----------------------------------------------------------------------------------------------
class Message_client_get_user_settings(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
    
#----------------------------------------------------------------------------------------------
class Message_client_set_user_settings(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
#----------------------------------------------------------------------------------------------
class Message_client_get_category_info(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
    