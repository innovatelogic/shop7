import wx
from categories_controller_panel import CategoriesControllerPanel
from category_trees_panel import CategoryTreesPanel, EPanelCategory
from groups_tree_view import GroupsTreeView

#----------------------------------------------------------------------------------------------
class CategoriesMainPanel(wx.Panel):
    LABEL_SHOW_WHOLE_TREE = "Show all tree"
    def __init__(self,
                 cases_controller,
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.realm = cases_controller.realm()
        self.base_aspects = self.realm.get_aspects()
        self.active_aspect_idx = ''
        
        self.doLayout()
        self.bottompanel.PopulateBaseList()
        
#----------------------------------------------------------------------------------------------        
    def doLayout(self):
        self.toppanel = CategoriesControllerPanel(self.cases_controller,
                                                  self.callback_ToggleBaseAspect,
                                                  self.callback_ToggleSecondAspect,
                                                  self.callback_OnClickSelectSecondAspect,
                                                  self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        
        self.bottompanel = CategoryTreesPanel(self.cases_controller, self, wx.ID_ANY)
        
        posCenterPanelVertSzr = wx.BoxSizer(wx.VERTICAL)
        posCenterPanelVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posCenterPanelVertSzr.Add(self.bottompanel, 1, wx.GROW)
        
        self.SetSizer(posCenterPanelVertSzr)
        self.Layout()
        
#----------------------------------------------------------------------------------------------        
    def initPopupMenu(self):
        user_settings = self.realm.getUserSettings()
        self.popupmenu = wx.Menu()
        radios = []
        for aspect in self.base_aspects:
            radio = wx.MenuItem(self.popupmenu, -1, text = aspect, kind = wx.ITEM_RADIO)
            self.popupmenu.AppendItem(radio)
            self.popupmenu.Check(radio.GetId(), self.active_aspect_idx == aspect)
            self.Bind(wx.EVT_MENU, self.OnPopupItemAspectSelected, radio)
            
        self.popupmenu.AppendSeparator()
        item_show_all = self.popupmenu.AppendCheckItem(-1, self.LABEL_SHOW_WHOLE_TREE)
        self.Bind(wx.EVT_MENU, self.OnShowAllCategoryTree, item_show_all)
        
        show_whole_tree = user_settings.options['client']['ui']['cases']['show_base_aspect_whole_tree']
        self.popupmenu.Check(item_show_all.GetId(), show_whole_tree)

#----------------------------------------------------------------------------------------------        
    def initSecondaryAspectList(self, aspect_id):
        self.PopulateSecondaryList(aspect_id)
        
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
    def SwitchPanel(self, index):
        self.bottompanel.TogglePanel(index)
        
#----------------------------------------------------------------------------------------------        
    def OnShowPopup(self, pos):
        cl_pos = self.ScreenToClient(pos)
        self.initPopupMenu()
        self.PopupMenu(self.popupmenu, cl_pos)
        
#----------------------------------------------------------------------------------------------        
    def OnPopupItemAspectSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        self.cases_controller.setActiveSecondaryAspect(item.GetText())

#----------------------------------------------------------------------------------------------            
    def OnShowAllCategoryTree(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        self.cases_controller.showAllCategoryTree(item.IsChecked())
        
#----------------------------------------------------------------------------------------------            
    def PopulateSecondaryList(self, aspect_id):
        self.active_aspect_idx = aspect_id
        self.bottompanel.PopulateSecondaryList(aspect_id)
        self.toppanel.SetSecondAspectName(aspect_id)