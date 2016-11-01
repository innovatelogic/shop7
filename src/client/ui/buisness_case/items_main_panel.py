import wx
from items_controller_panel import ItemsControllerPanel
from items_list_panel import ItemsListPanel

class ItemsMainPanel(wx.Panel):
    def __init__(self, realm, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = realm
        self.doLayout()
        
    def doLayout(self):
        self.toppanel = ItemsControllerPanel(self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        self.bottompanel = ItemsListPanel(self.realm, self, wx.ID_ANY)
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.toppanel, 0, wx.EXPAND)
        vsizer.Add(self.bottompanel, 1, wx.GROW)
        
        self.SetSizer(vsizer)

        self.Layout()