
class BuisnessCaseController():
    ITEMS_PER_PAGE = 5
    
    def __init__(self, realm):
        self.__realm = realm
        self.view = None
        self.items_offset = 0
        self.items_per_page = 0
        
#----------------------------------------------------------------------------------------------        
    def setView(self, view):
        self.view = view

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
    def showAllCategoryTree(self, flag):
        user_settings = self.__realm.get_user_settings()
        user_settings.options['client']['ui']['cases']['show_base_aspect_whole_tree'] = flag
        self.__realm.set_user_settings(user_settings)
        
#----------------------------------------------------------------------------------------------    
    def itemColumnChange(self, text, flag):
        print('[item_column_change]')
        user_settings = self.__realm.get_user_settings()
        if text in user_settings.options['client']['ui']['cases']['item_columns']:
            user_settings.options['client']['ui']['cases']['item_columns'][text] = flag
            self.__realm.set_user_settings(user_settings)
        pass

#----------------------------------------------------------------------------------------------        
    def toggleBaseAspect(self):
        pass
    
#----------------------------------------------------------------------------------------------    
    def toggleSecondAspect(self):
        pass
    
#----------------------------------------------------------------------------------------------    
    def populate_base_list(self):
        pass

#----------------------------------------------------------------------------------------------
    def expandUserAspectCategory(self, category_id, item):
        categories = self.__realm.get_user_category_childs(self.secondary_tree.GetPyData(item))
        self.view.addChildCategoriesTreeUserAspect(category_id, categories, item)
        pass
    
#----------------------------------------------------------------------------------------------
    def expandBaseAspectCategory(self, aspect, category_id, item):
        categories = self.__realm.get_category_childs(aspect, category_id)
        self.view.addChildCategoriesTreeBaseAspect(category_id, categories, item)
        pass
 
#----------------------------------------------------------------------------------------------
    def categoryUserAspectSelected(self, category_id):
        print("[categoryUserAspectSelected]")
        pass
    
#----------------------------------------------------------------------------------------------
    def categoryBaseAspectSelected(self, aspect, category_id):
        ''' process user category selection'''
        info = self.__realm.get_category_info(aspect, category_id)
        state = self.__realm.get_items_category_state()
        
        if state.getCategoryId() != category_id:
            state.set(aspect, category_id, info['items_num'], self.ITEMS_PER_PAGE)

            self.view.initPageController(state)
            self.updateItemsPage()
        pass

#----------------------------------------------------------------------------------------------
    def updateItemsPage(self):
        state = self.__realm.get_items_category_state()
        items = self.__realm.get_items(state.getAspect(), state.getCategoryId(), state.getOffset(), self.ITEMS_PER_PAGE)
        self.view.fillItemsList(items)
        
    #----------------------------------------------------------------------------------------------    
    def page_inc(self):
        state = self.__realm.get_items_category_state()
        if state.inc_page():
            self.view.updatePageController(state)
            self.updateItemsPage()
        pass

#----------------------------------------------------------------------------------------------    
    def page_dec(self):
        state = self.__realm.get_items_category_state()
        if state.dec_page():
            self.view.updatePageController(state)
            self.updateItemsPage()
        pass
    
#----------------------------------------------------------------------------------------------
    def page_select(self, page_index):
        print('[page_select]')
        pass