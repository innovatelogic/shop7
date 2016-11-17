

class ItemsCacheModel():
    def __init__(self, db_instance):
        self.db_instance = db_instance
        pass
    
    def get_items(self, token, category_id, offset):
        out = []
        items = self.db_instance.items.get_user_items(token, category_id, offset)
        
        for item in items:
            out.append(item.get())
        return out
        
    def get_item(self, token, _id):
        return self.db_instance.items.get_item(_id)
        
    