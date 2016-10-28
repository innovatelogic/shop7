import wx
from items_controller_panel import ItemsControllerPanel

class ItemsMainPanel(wx.Panel):
    def __init__(self, connection_info, ms_connection, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.connection_info = connection_info
        self.ms_connection = ms_connection 
        
        self.doLayout()
        
    def doLayout(self):
        self.toppanel = ItemsControllerPanel(self.connection_info, self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        
        self.bottompanel = wx.Panel(self, wx.ID_ANY)
        
        posCenterPanelVertSzr = wx.BoxSizer(wx.VERTICAL)
        posCenterPanelVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posCenterPanelVertSzr.Add(self.bottompanel, 1, wx.GROW)
        
        self.SetSizer(posCenterPanelVertSzr)

        self.Layout()