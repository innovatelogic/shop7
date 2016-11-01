import wx
from categories_controller_panel import CategoriesControllerPanel
from category_trees_panel import CategoryTreesPanel
from groups_tree_view import GroupsTreeView

class CategoriesMainPanel(wx.Panel):
    def __init__(self, realm, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = realm
        
        self.doLayout()
        
    def doLayout(self):
        self.toppanel = CategoriesControllerPanel(self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        
        self.bottompanel = CategoryTreesPanel(self.realm, self, wx.ID_ANY)
        
        posCenterPanelVertSzr = wx.BoxSizer(wx.VERTICAL)
        posCenterPanelVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posCenterPanelVertSzr.Add(self.bottompanel, 1, wx.GROW)
        
        self.SetSizer(posCenterPanelVertSzr)

        self.Layout()
        
    def SwitchPanel(self, index):
        self.bottompanel.TogglePanel(index)