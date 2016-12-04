class ItemsController():
    def __init__(self):
        self.items_count = 0
        self.offset = 0
        
    def set(self, count, offset):
        self.items_count = count
        self.offset = offset
        
    def get_count(self):
        return self.items_count
        
    def set_offset(self, offset):
        self.offset = offset
        
    def get_offset(self):
        return self.offset