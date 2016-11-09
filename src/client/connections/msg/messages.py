import pika

class Message():
    def __init__(self, connection_info, channel, callback_queue, get, send):
        self.channel = channel
        self.connection_info = connection_info
        self.callback_queue = callback_queue
        self.send_params = []
        self.get_params = []
        self.__parse(get, send)
        pass
    
    def __parse(self, get, send):
        arr = get.split(";")
        for s in arr:
            self.get_params.append(s)
        arr = send.split(";")
        for s in arr:
            self.send_params.append(s)
            
    def send(self, params, corr_id):
        params = self.update_params(params)
        
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

    def update_params(self, params):
        params['opcode'] = 'auth_activate'
        params['token'] = self.connection_info['token']
        return params
#----------------------------------------------------------------------------------------------  
class Message_client_logout(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

    def update_params(self, params):
        params['opcode'] = 'logout'
        params['token'] = self.connection_info['token']
        return params

#----------------------------------------------------------------------------------------------       
class Message_client_get_categiries_1st_lvl(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def update_params(self, params):
        params['opcode'] = 'get_categiries_1st_lvl'
        params['token'] = self.connection_info['token']
        return params

#----------------------------------------------------------------------------------------------       
class Message_client_get_category_childs(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def update_params(self, params):
        params['opcode'] = 'get_category_childs'
        params['token'] = self.connection_info['token']
        return params
    
#----------------------------------------------------------------------------------------------       
class Message_client_get_items(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def update_params(self, params):
        params['opcode'] = 'get_items'
        params['token'] = self.connection_info['token']
        return params

#----------------------------------------------------------------------------------------------       
class Message_client_get_aspects(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def update_params(self, params):
        params['opcode'] = 'get_aspects'
        params['token'] = self.connection_info['token']
        return params    