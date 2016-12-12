from add_item.add_item_controller import AddItemController

class BuisnessCaseController():
    ITEMS_PER_PAGE = 5
    USER_ASPECT_FLAG = '__USER_ASPECT__'
    
    def __init__(self, realm):
        self.__realm = realm
        self.view = None
        self.items_offset = 0
        self.items_per_page = 0
        self.addItemController = AddItemController(self)

#----------------------------------------------------------------------------------------------        
    def setView(self, view):
        self.view = view

#----------------------------------------------------------------------------------------------
    def getView(self):
        return self.view

#----------------------------------------------------------------------------------------------
    def realm(self):
        return self.__realm
    
#----------------------------------------------------------------------------------------------    
    def getAddItemController(self):
        return self.addItemController
    
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
    def addItem(self):
        res = False
        if self.view.addItem():
            self.getAddItemController().start()
            res = True
        return res

#----------------------------------------------------------------------------------------------    
    def editItem(self):
        self.view.editItem()
        pass

#----------------------------------------------------------------------------------------------
    def delItem(self):
        self.view.delItem()
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
        info = self.__realm.get_user_category_info(category_id)
        state = self.__realm.get_items_category_state()
        
        print category_id
        if state.getCategoryId() != category_id:
            state.set(self.USER_ASPECT_FLAG, category_id, info['items_num'], self.ITEMS_PER_PAGE)
            self.view.initPageController(state)
            self.updateItemsPage()
        print info
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
        aspect = state.getAspect()
        items = []
        if aspect == self.USER_ASPECT_FLAG:
            items = self.__realm.get_user_category_items(state.getCategoryId(), state.getOffset(), self.ITEMS_PER_PAGE)
        else:
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