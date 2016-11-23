
class BuisnessCaseController():
    def __init__(self, realm):
        self.__realm = realm

#----------------------------------------------------------------------------------------------        
    def realm(self):
        return self.__realm
    
#----------------------------------------------------------------------------------------------        
    def user_category_selected(self, cat_id):
        print('[user_category_selected]')

#----------------------------------------------------------------------------------------------        
    def secondary_category_selected(self, aspect, cat_id):
        print('[secondary_category_selected]')

#----------------------------------------------------------------------------------------------        
    def show_all_category_tree_selected(self, flag):
        print('[show_all_category_tree_selected]')

#----------------------------------------------------------------------------------------------    
    def add_item(self):
        print('[add_item]')
        pass
    
#----------------------------------------------------------------------------------------------    
    def edit_item(self):
        print('[edit_item]')
        pass
    
#----------------------------------------------------------------------------------------------
    def del_item(self):
        print('[del_item]')
        pass
    
#----------------------------------------------------------------------------------------------    
    def column_check(self, text, flag):
        print('[column_check]')
        pass

#----------------------------------------------------------------------------------------------    
    def page_inc(self):
        print('[callback_page_inc]')
        pass

#----------------------------------------------------------------------------------------------    
    def page_dec(self):
        print('[callback_page_dec]')
        pass
    
#----------------------------------------------------------------------------------------------
    def page_select(self, page_index):
        print('[page_select]')
        pass

#----------------------------------------------------------------------------------------------        
    def toggleBaseAspect(self):
        pass
    
#----------------------------------------------------------------------------------------------    
    def toggleSecondAspect(self):
        pass
    
    def populate_base_list(self):
        pass
        
        