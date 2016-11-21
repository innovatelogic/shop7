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

        res = None
        if dict['aspect'] == '':
            res = self.master.realm().users_model.get_first_level_categories(dict['token'])
        else:
            user_group_id = self.master.realm().users_model.get_group_id_by_token(dict['token'])
            category_root = self.master.realm().base_aspects_container.get_aspect_category_root(dict['aspect'])
            
            res = []
            res.append({'_id':str(category_root.category._id), 
                        'parent_id': str(category_root.category.parent_id),
                        'name':category_root.category.name, 
                        'n_childs':str(len(category_root.childs))})
            
            childs = self.master.realm().base_aspects_container.get_aspect_child_categories(dict['aspect'], category_root.category._id)
            
            for child in childs:
                if self.master.realm().category_group_items_cache.get_item_count(dict['aspect'], child.category._id, user_group_id) > 0:
                    res.append({'_id':str(child.category._id), 
                            'parent_id': str(child.category.parent_id),
                            'name':child.category.name, 
                            'n_childs':str(len(child.childs))})
        return res

#----------------------------------------------------------------------------------------------       
class Message_server_get_category_childs(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        dict = eval(body)
        res = []
        if dict['aspect'] == '':
            res = self.master.realm().users_model.get_child_categories(dict['token'], dict['id'])
        else:
            user_group_id = self.master.realm().users_model.get_group_id_by_token(dict['token'])
            category_root = self.master.realm().base_aspects_container.get_aspect_category_root(dict['aspect'])
            
            childs = self.master.realm().base_aspects_container.get_aspect_child_categories(dict['aspect'], dict['id'])
            for child in childs:
                if self.master.realm().category_group_items_cache.get_item_count(dict['aspect'], child.category._id, user_group_id) > 0:
                    res.append({'_id':str(child.category._id), 
                            'parent_id': str(child.category.parent_id),
                            'name':child.category.name, 
                            'n_childs':str(len(child.childs))})
            
            #res = self.master.realm().base_aspects_container.get_child_categories(dict['aspect'], dict['id'])
        return res
    
#----------------------------------------------------------------------------------------------       
class Message_server_get_items(Message):
    def __init__(self, *args, **kwargs):
        Message.__init__(self, *args, **kwargs)
        
    def do_process(self, ch, method, props, body):
        dict = eval(body)
        
        mappings = self.master.realm().db.items_mapping.get_mappings_by_aspect_category('prom_ua', dict['category_id'])
        
        items = []
        for mapping in mappings:
            item = self.master.realm().items_cache_model.get_item(dict['token'], mapping['item_id'])
            if item:
                items.append(item.get())
            else:
                print('[Message_server_get_items] failed get item {}'.format(mapping['item_id']))

        return items

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