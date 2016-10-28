import wx
from categories_controller import CategoriesControllerPanel
from category_trees_panel import CategoryTreesPanel
from groups_tree_view import GroupsTreeView

class CategoriesMainPanel(wx.Panel):
    def __init__(self, connection_info, ms_connection, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.connection_info = connection_info
        self.ms_connection = ms_connection 
        #self.SetBackgroundColour((34, 65, 96))
        
        self.doLayout()
        
    def doLayout(self):
        self.toppanel = CategoriesControllerPanel(self.connection_info, self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        
        self.bottompanel = CategoryTreesPanel(self.ms_connection, self, wx.ID_ANY)
        
        posCenterPanelVertSzr = wx.BoxSizer(wx.VERTICAL)
        posCenterPanelVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posCenterPanelVertSzr.Add(self.bottompanel, 1, wx.GROW)
        
        self.SetSizer(posCenterPanelVertSzr)

        self.Layout()
        
    def SwitchPanel(self, index):
        self.bottompanel.TogglePanel(index)