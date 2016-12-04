class ItemsCategoryState():
    def __init__(self):
        self.items_count = 0
        self.offset = 0
        self.aspect = ''
        self.category_id = 0
        self.selected_items = []

#----------------------------------------------------------------------------------------------
    def set(self, aspect, category_id, count, offset = 0):
        self.aspect = aspect
        self.category_id = category_id
        self.items_count = count
        self.offset = offset
        
#----------------------------------------------------------------------------------------------
    def getAspect(self):
        return self.aspect
    
#----------------------------------------------------------------------------------------------
    def getCategoryId(self):
        return self.category_id

#----------------------------------------------------------------------------------------------
    def get_count(self):
        return self.items_count

#----------------------------------------------------------------------------------------------
    def set_offset(self, offset):
        self.offset = offset

#----------------------------------------------------------------------------------------------
    def get_offset(self):
        return self.offset