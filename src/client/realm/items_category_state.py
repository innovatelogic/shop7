class ItemsCategoryState():
    def __init__(self):
        self.items_count = 0
        self.items_on_page = 0
        self.page_count = 0
        self.current_page = 0 # 1 based digit. 0 state not initialized
        self.offset = 0
        self.aspect = ''
        self.category_id = 0
        self.selected_items = []

#----------------------------------------------------------------------------------------------
    def set(self, aspect, category_id, count, items_per_page = 10):
        self.aspect = aspect
        self.category_id = category_id
        self.items_count = count
        self.offset = 0
        self.items_on_page = items_per_page

        page_count = float(count) / self.items_on_page
        if page_count > int(page_count):
            page_count = int(page_count) + 1
        self.page_count = int(page_count)
        self.curr_page = 1
        
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
    def getOffset(self):
        return self.offset
    
#----------------------------------------------------------------------------------------------
    def getPageCount(self):
        return self.page_count

#----------------------------------------------------------------------------------------------
    def inc_page(self):
        res = False
        if self.curr_page < self.page_count:
            self.curr_page += 1
            self.offset = (self.curr_page - 1) * self.items_on_page
            res = True
        return res
    
#----------------------------------------------------------------------------------------------
    def dec_page(self):
        res = False
        if self.curr_page > 1:
            self.curr_page -= 1
            self.offset = (self.curr_page - 1) * self.items_on_page
            res = True
        return res
    
#----------------------------------------------------------------------------------------------
    def getCurrPage(self):
        return self.curr_page