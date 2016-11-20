import wx
from categories_controller_panel import CategoriesControllerPanel
from category_trees_panel import CategoryTreesPanel, EPanelCategory
from groups_tree_view import GroupsTreeView

#----------------------------------------------------------------------------------------------
class CategoriesMainPanel(wx.Panel):
    LABEL_SHOW_WHOLE_TREE = "Show all tree"
    def __init__(self,
                 realm, 
                 callback_user_cat_selected,
                 callback_secondary_cat_selected,
                 callback_show_all_category_tree_selected,
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = realm
        self.callback_user_cat_selected = callback_user_cat_selected
        self.callback_secondary_cat_selected = callback_secondary_cat_selected
        self.callback_show_all_category_tree_selected = callback_show_all_category_tree_selected
        self.base_aspects = self.realm.get_aspects()
        self.active_aspect_idx = -1
        
        self.doLayout()
        self.bottompanel.PopulateBaseList()
        
#----------------------------------------------------------------------------------------------        
    def doLayout(self):
        self.toppanel = CategoriesControllerPanel(self.callback_ToggleBaseAspect,
                                                  self.callback_ToggleSecondAspect,
                                                  self.callback_OnClickSelectSecondAspect,
                                                  self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        
        self.bottompanel = CategoryTreesPanel(self.realm, 
                                              self.callback_user_cat_selected,
                                              self.callback_secondary_cat_selected,
                                              self, wx.ID_ANY)
        
        posCenterPanelVertSzr = wx.BoxSizer(wx.VERTICAL)
        posCenterPanelVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posCenterPanelVertSzr.Add(self.bottompanel, 1, wx.GROW)
        
        self.SetSizer(posCenterPanelVertSzr)
        self.initPopupMenu()
        self.Layout()
        
        self.initSecondaryAspectList()
        
#----------------------------------------------------------------------------------------------        
    def initPopupMenu(self):
        user_settings = self.realm.get_user_settings()
        
        self.popupmenu = wx.Menu()
        radios = []
        for aspect in self.base_aspects:
            radio = wx.MenuItem(self.popupmenu, -1, text = aspect, kind = wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, radio)
            self.popupmenu.AppendItem(radio)
            
        self.popupmenu.AppendSeparator()
        item_show_all = self.popupmenu.AppendCheckItem(-1, self.LABEL_SHOW_WHOLE_TREE)
        self.Bind(wx.EVT_MENU, self.OnShowAllCategoryTree, item_show_all)
        
        self.popupmenu.Check(item_show_all.GetId(), user_settings['client']['ui']['cases']['show_base_aspect_whole_tree'])

#----------------------------------------------------------------------------------------------        
    def initSecondaryAspectList(self):
        try:
            idx = self.base_aspects.index(self.realm.get_user_settings()['client']['ui']['cases']['active_base_aspect'])
        except ValueError:
            idx = 0
        self.PopulateSecondaryList(idx)
        
#----------------------------------------------------------------------------------------------        
    def callback_ToggleBaseAspect(self):
        self.SwitchPanel(EPanelCategory.EPanel_Base)
        pass
    
#----------------------------------------------------------------------------------------------    
    def callback_ToggleSecondAspect(self):
        self.SwitchPanel(EPanelCategory.EPanel_Secondary)
        pass
    
#----------------------------------------------------------------------------------------------    
    def callback_OnClickSelectSecondAspect(self, pos):
        self.OnShowPopup(pos)
        pass
    
#----------------------------------------------------------------------------------------------    
    def callback_OnClickShowAllCategoryTree(self, flag):
        #self.callback_show_all_category_tree_selected(flag)
        pass
    
#----------------------------------------------------------------------------------------------        
    def SwitchPanel(self, index):
        self.bottompanel.TogglePanel(index)
        
#----------------------------------------------------------------------------------------------        
    def OnShowPopup(self, pos):
        cl_pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, cl_pos)
        
#----------------------------------------------------------------------------------------------        
    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        for i in range(len(self.base_aspects)):
            if self.base_aspects[i] == text:
                self.PopulateSecondaryList(i)
                break

#----------------------------------------------------------------------------------------------            
    def OnShowAllCategoryTree(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        self.callback_show_all_category_tree_selected(item.IsChecked())
        
#----------------------------------------------------------------------------------------------            
    def PopulateSecondaryList(self, index):
        if index >= 0 and index < len(self.base_aspects):
            if index != self.active_aspect_idx:
                self.active_aspect_idx = index
                self.bottompanel.PopulateSecondaryList(self.base_aspects[index])
                self.toppanel.SetSecondAspectName(self.base_aspects[index])