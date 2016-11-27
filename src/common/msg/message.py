import pika
#from wx.lib.pubsub.core import kwargs

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
        
        return self.master.realm().users_model.activateUserAuth(dict['token'])

#----------------------------------------------------------------------------------------------
class Message_server_logout(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

    def do_process(self, ch, method, props, body):
        dict = eval(body)
        return self.master.realm().users_model.logoutUser(dict['token'])

#----------------------------------------------------------------------------------------------
class Message_server_get_categiries_1st_lvl(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        dict = eval(body)          
        return self.master.realm().get_categories_1st_lvl(dict['token'], dict['aspect'])

#----------------------------------------------------------------------------------------------
class Message_server_get_category_childs(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        dict = eval(body)
        return self.master.realm().get_category_childs(dict['token'], dict['aspect'], dict['id'])
    
#----------------------------------------------------------------------------------------------
class Message_server_get_items(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        dict = eval(body)
        return self.master.realm().get_items(dict['token'], 'prom_ua', dict['category_id'])

#----------------------------------------------------------------------------------------------
class Message_server_get_aspects(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        return self.master.realm().base_aspects_container.get_aspects()

#----------------------------------------------------------------------------------------------  
class Message_server_get_user_settings(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        dict = eval(body)
        settings = self.master.realm().users_model.get_user_settings(dict['token'])
        if settings:
            return settings.get()
        return {}
    
#----------------------------------------------------------------------------------------------  
class Message_server_set_user_settings(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        dict = eval(body)
        return self.master.realm().users_model.set_user_settings(dict['token'], dict['settings'])