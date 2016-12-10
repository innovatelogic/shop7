import wx
from add_item_top_panel import AddItemTopPanel

#----------------------------------------------------------------------------------------------
class AddItemMainPanel(wx.Panel):
    def __init__(self, cases_controller, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.doLayout()
        pass

#----------------------------------------------------------------------------------------------
    def doLayout(self):
        self.toppanel = AddItemTopPanel(self.cases_controller, self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        self.bottompanel = wx.Panel(self, wx.ID_ANY)
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.toppanel, 0, wx.EXPAND)
        vsizer.Add(self.bottompanel, 1, wx.GROW)
        
        self.toppanel.SetBackgroundColour(wx.Colour(34, 0, 0))
        self.bottompanel.SetBackgroundColour(wx.Colour(0, 0, 96))
        
        self.SetSizer(vsizer)
        self.Layout()