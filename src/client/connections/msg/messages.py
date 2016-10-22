import pika

class Message():
    def __init__(self, get, send):
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
            
#----------------------------------------------------------------------------------------------  
class Message_client_logout(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)

    def do_process(self, ch, method, props, body):
        pass

#----------------------------------------------------------------------------------------------       
class Message_client_get_groups(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        pass

#----------------------------------------------------------------------------------------------       
class Message_client_get_category_childs(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        pass