import wx
from categories_controller_panel import CategoriesControllerPanel
from category_trees_panel import CategoryTreesPanel, EPanelCategory
from groups_tree_view import GroupsTreeView

class CategoriesMainPanel(wx.Panel):
    def __init__(self, realm, callback_cat_selected, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = realm
        self.callback_cat_selected = callback_cat_selected
        
        self.doLayout()
        
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
        
        self.popupmenu = wx.Menu()
        for text in "one two three four five".split():
            item = self.popupmenu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
        #self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)
        
        self.Layout()
        
    def BindEvents(self):
        pass
    
    def callback_ToggleBaseAspect(self):
        self.SwitchPanel(EPanelCategory.EPanel_Base)
        pass
    
    def callback_ToggleSecondAspect(self):
        self.SwitchPanel(EPanelCategory.EPanel_Secondary)
        pass
    
    def callback_OnClickSelectSecondAspect(self):
        print('callback_OnClickSelectSecondAspect')
        self.OnShowPopup()
        pass
        
    def SwitchPanel(self, index):
        self.bottompanel.TogglePanel(index)
        
    def OnShowPopup(self):
        pos = wx.GetMousePosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)
        
    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        wx.MessageBox("You selected item '%s'" % text)