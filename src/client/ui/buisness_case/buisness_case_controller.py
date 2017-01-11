from add_item.add_item_controller import AddItemController

ON_SECOND_ASPECT_CHANGED = 1
    
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class BuisnessCaseController():
    ITEMS_PER_PAGE = 5
    USER_ASPECT_FLAG = '__USER_ASPECT__'
    
    class Event():
        def __init__(self, func):
            self.funcs = [func]
        def fire(self):
            for i in self.runcs():
                i()
    
    def __init__(self, realm):
        self.__realm = realm
        self.view = None
        self.items_offset = 0
        self.items_per_page = 0
        self.addItemController = AddItemController(self)
        self.events = {}

#----------------------------------------------------------------------------------------------
    def init(self):
        self.view.setSecondAspect(self.getActiveSecondaryAspect())
        pass

#----------------------------------------------------------------------------------------------
    def getActiveSecondaryAspect(self):
        return self.__realm.getUserSettings().options['client']['ui']['cases']['active_base_aspect']
    
#----------------------------------------------------------------------------------------------
    def addEvent(self, ID, func):
        if str(ID) not in self.events:
            self.events[str(ID)] = Event(func)
        else:
            self.events[ID].funcs.append(func)
             
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
        user_settings = self.__realm.getUserSettings()
        user_settings.options['client']['ui']['cases']['show_base_aspect_whole_tree'] = flag
        self.__realm.set_user_settings(user_settings)
        
#----------------------------------------------------------------------------------------------
    def itemColumnChange(self, text, flag):
        user_settings = self.__realm.getUserSettings()
        if text in user_settings.options['client']['ui']['cases']['item_columns']:
            user_settings.options['client']['ui']['cases']['item_columns'][text] = flag
            self.__realm.set_user_settings(user_settings)
        self.view.updateItemList()
        
#----------------------------------------------------------------------------------------------
    def toggleItemPreviewColumn(self, flag):
        user_settings = self.__realm.getUserSettings()
        user_settings.options['client']['ui']['cases']['item_preview_column'] = flag
        self.__realm.set_user_settings(user_settings)
        self.view.toggleItemPreveiewColumn(flag)
        
#----------------------------------------------------------------------------------------------
    def setActiveSecondaryAspect(self, aspect):
        user_settings = self.__realm.getUserSettings()
        user_settings.options['client']['ui']['cases']['active_base_aspect'] = aspect
        self.__realm.set_user_settings(user_settings)
        self.view.setSecondAspect(self.getActiveSecondaryAspect())
        pass

#----------------------------------------------------------------------------------------------        
    def toggleBaseAspect(self, aspect_id):
        pass
    
#----------------------------------------------------------------------------------------------    
    def toggleSecondAspect(self):
        pass
    
#----------------------------------------------------------------------------------------------    
    def populate_base_list(self):
        pass

#----------------------------------------------------------------------------------------------
    def expandUserAspectCategory(self, category_id, item):
        categories = self.__realm.get_user_category_childs(category_id)
        self.view.addChildCategoriesTreeUserAspect(category_id, categories, item)
        pass
    
#----------------------------------------------------------------------------------------------
    def expandBaseAspectCategory(self, category_id, item):
        aspect = self.getActiveSecondaryAspect()
        categories = self.__realm.get_category_childs(aspect, category_id)
        self.view.addChildCategoriesTreeBaseAspect(category_id, categories, item)
        pass
 
#----------------------------------------------------------------------------------------------
    def categoryUserAspectSelected(self, category_id):
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
    def categoryBaseAspectSelected(self, category_id):
        ''' process user category selection'''

        aspect = self.getActiveSecondaryAspect()
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

#----------------------------------------------------------------------------------------------
    def getItemsListInfo(self):
        user_settings = self.__realm.getUserSettings()
        
        dsc = user_settings.options['client']['ui']['cases']['item_columns']
        
        info = [('#', True),
                ('Img', dsc['image']),
                ('Name', dsc['name']),
                ('Availability', dsc['availability']),
                ('Amount', dsc['amount']),
                ('Unit', dsc['unit']),
                ('Price', dsc['price']),
                ('Currency', dsc['currency']),
                ('Desc', dsc['desc'])]
        
        return info
    