import wx
from groups_tree_view import GroupsTreeView

class EPanelCategory:
    EPanel_Base = 0
    EPanel_Secondary = 1
    EPanel_MAX = 2

class CategoryTreesPanel(wx.Panel):
    def __init__(self, ms_connection, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.ms_connection = ms_connection 
        self.SetBackgroundColour((255, 0, 0))
        self.view_panels = []
        self.doLayout()
        
    def doLayout(self):
        #self.left_tree = GroupsTreeView(self.ms_connection, 
        #                                        self, 1, wx.DefaultPosition, (-1, -1),
        #                                        wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT)
        
        self.base_panel = wx.Panel(self, wx.ID_ANY, size = (-1, -1))
        self.secondary_panel = wx.Panel(self, wx.ID_ANY, size = (-1, -1))
        
        self.base_panel.SetBackgroundColour((54, 45, 54))
        self.secondary_panel.SetBackgroundColour((255, 45, 23))
        
        self.view_panels.append(self.base_panel)
        self.view_panels.append(self.secondary_panel)
        
        self.gridsizer = wx.FlexGridSizer(cols=1, rows = 1)
        self.gridsizer.AddGrowableRow(0)
        self.gridsizer.AddGrowableCol(0)
      
        self.TogglePanel(EPanelCategory.EPanel_Base)
        
        self.SetSizer(self.gridsizer)
        
        self.Layout()
        
    def TogglePanel(self, index):
        out = None
        self.gridsizer.Clear()
        for i in range(0, EPanelCategory.EPanel_MAX):
            if i == index:
                self.gridsizer.Add(self.view_panels[i], 0, wx.EXPAND)
                self.view_panels[i].Show()
                self.view_panels[i].Layout()
                out = self.view_panels[i]
            else:
                self.view_panels[i].Hide()
        self.Layout()
        return out