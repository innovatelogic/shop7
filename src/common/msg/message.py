import pika

class Message():
    def __init__(self, master, get, send):
        self.send_params = []
        self.get_params = []
        self.master = master
        self.__parse(get, send)
        pass
    
    def __parse(self, get, send):
        arr = get.split(";")
        for s in arr:
            self.get_params.append(s)
        arr = send.split(";")
        for s in arr:
            self.send_params.append(s)
        
    def process(self, ch, method, props, body):
        result = self.do_process(ch, method, props, body)
        
        reply = str({'res': result})

        ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=reply)

#----------------------------------------------------------------------------------------------
class Message_server_auth_activate(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

    def do_process(self, ch, method, props, body):
        dict = eval(body)
        
        return self.master.users_model.activateUserAuth(dict['token'])

#----------------------------------------------------------------------------------------------  
class Message_server_logout(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

    def do_process(self, ch, method, props, body):
        dict = eval(body)
        return self.master.users_model.logoutUser(dict['token'])

#----------------------------------------------------------------------------------------------       
class Message_server_get_groups(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        dict = eval(body)
        return self.master.base_aspects_container.get_first_level_categories('prom_ua')

#----------------------------------------------------------------------------------------------       
class Message_server_get_category_childs(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        dict = eval(body)
        return self.master.base_aspects_container.get_childs('prom_ua', dict['id'])
    
    #----------------------------------------------------------------------------------------------       
class Message_server_get_items(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        dict = eval(body)
        return self.master.items_cache_model.get_items(dict['token'], dict['category_id'], dict['offset'])
