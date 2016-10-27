import wx
from buisness_case.categories_controller import CategoriesControllerPanel

class CategoriesControlPanel(wx.Panel):
    def __init__(self, connection_info, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.connection_info = connection_info
        #self.SetBackgroundColour((34, 65, 96))
        
        self.doLayout()
        
    def doLayout(self):
        self.toppanel = CategoriesControllerPanel(self.connection_info, self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        
        self.bottompanel = wx.Panel(self, wx.ID_ANY)
        self.bottompanel.SetBackgroundColour((0, 0, 255))
        
        posCenterPanelVertSzr = wx.BoxSizer(wx.VERTICAL)
        posCenterPanelVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posCenterPanelVertSzr.Add(self.bottompanel, 1, wx.GROW)
        
        self.SetSizer(posCenterPanelVertSzr)
        
        self.Layout()