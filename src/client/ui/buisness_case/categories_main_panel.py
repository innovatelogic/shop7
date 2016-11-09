import wx
from categories_controller_panel import CategoriesControllerPanel
from category_trees_panel import CategoryTreesPanel, EPanelCategory
from groups_tree_view import GroupsTreeView

class CategoriesMainPanel(wx.Panel):
    def __init__(self, realm, callback_cat_selected, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = realm
        self.callback_cat_selected = callback_cat_selected
        self.base_aspects = self.realm.get_aspects()
        self.active_aspect_idx = -1
        
        self.doLayout()
        
        self.bottompanel.PopulateBaseList()
        self.PopulateSecondaryList(0)
        
    def doLayout(self):
        self.toppanel = CategoriesControllerPanel(self.callback_ToggleBaseAspect,
                                                  self.callback_ToggleSecondAspect,
                                                  self.callback_OnClickSelectSecondAspect,
                                                  self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        self.bottompanel = CategoryTreesPanel(self.realm, self.callback_cat_selected, self, wx.ID_ANY)
        
        posCenterPanelVertSzr = wx.BoxSizer(wx.VERTICAL)
        posCenterPanelVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posCenterPanelVertSzr.Add(self.bottompanel, 1, wx.GROW)
        
        self.SetSizer(posCenterPanelVertSzr)
        
        self.initPopup()
        
        self.Layout()
        
    def initPopup(self):
        self.popupmenu = wx.Menu()
        print self.base_aspects
        for aspect in self.base_aspects:
            item = self.popupmenu.Append(-1, aspect)
            self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
        
    def callback_ToggleBaseAspect(self):
        self.SwitchPanel(EPanelCategory.EPanel_Base)
        pass
    
    def callback_ToggleSecondAspect(self):
        self.SwitchPanel(EPanelCategory.EPanel_Secondary)
        pass
    
    def callback_OnClickSelectSecondAspect(self, pos):
        #print('callback_OnClickSelectSecondAspect')
        self.OnShowPopup(pos)
        pass
        
    def SwitchPanel(self, index):
        self.bottompanel.TogglePanel(index)
        
    def OnShowPopup(self, pos):
        cl_pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, cl_pos)
        
    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        #wx.MessageBox(("You selected item {}").format(event.GetId()))
        for i in range(len(self.base_aspects)):
            if self.base_aspects[i] == text:
                self.PopulateSecondaryList(i)
                break
        
    def PopulateSecondaryList(self, index):
        if index >= 0 and index < len(self.base_aspects):
            if index != self.active_aspect_idx:
                self.active_aspect_idx = index
                self.bottompanel.PopulateSecondaryList(self.base_aspects[index])
                self.toppanel.SetSecondAspectName(self.base_aspects[index])