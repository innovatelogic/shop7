
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
        
        info = self.__realm.get_category_info(aspect, category_id)
        category_ctrl = self.__realm.get_items_category_state()
        
        if category_ctrl.getCategoryId() != category_id:
            self.__realm.set_items_category_state(aspect, category_id, info['items_num'], 0)
        
            page_count = float(info['items_num']) / self.ITEMS_PER_PAGE
            if page_count > int(page_count):
                page_count = int(page_count) + 1
            
            self.view.initPageController(int(page_count))
            self.updateItemsPage()
        pass

#----------------------------------------------------------------------------------------------
    def updateItemsPage(self):
        category_ctrl = self.__realm.get_items_category_state()
        items = self.__realm.get_items(category_ctrl.getAspect(), category_ctrl.getCategoryId(), 0, self.ITEMS_PER_PAGE)
        self.view.fillItemsList(items)