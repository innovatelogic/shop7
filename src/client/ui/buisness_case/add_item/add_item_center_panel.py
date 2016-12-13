import wx

#----------------------------------------------------------------------------------------------
class AddItemCenterPanel(wx.Panel):
    def __init__(self, 
                 cases_controller, 
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.view_panels = []
        self.doLayout()
        
#----------------------------------------------------------------------------------------------   
    def doLayout(self):
        self.SetBackgroundColour((255, 255, 255))
        
        self.first_page_panel = wx.Panel(self, wx.ID_ANY, size = (-1, -1))
        self.second_page_panel = wx.Panel(self, wx.ID_ANY, size = (-1, -1))
        self.third_page_panel = wx.Panel(self, wx.ID_ANY, size = (-1, -1))
        
        self.first_page_panel.SetBackgroundColour((255, 0, 0))
        self.second_page_panel.SetBackgroundColour((0, 255, 0))
        self.third_page_panel.SetBackgroundColour((0, 0, 255))
        
        self.view_panels.append(self.first_page_panel)
        self.view_panels.append(self.second_page_panel)
        self.view_panels.append(self.third_page_panel)
        
        self.gridsizer = wx.FlexGridSizer(cols=1, rows = 1)
        self.gridsizer.AddGrowableRow(0)
        self.gridsizer.AddGrowableCol(0)
      
        self.ToggleCenterPage(0)
        self.SetSizer(self.gridsizer)
        pass

#----------------------------------------------------------------------------------------------
    def ToggleCenterPage(self, index):
        out = None
        self.gridsizer.Clear()
        for i in range(0, len(self.view_panels)):
            if i == index:
                self.gridsizer.Add(self.view_panels[i], 0, wx.EXPAND)
                self.view_panels[i].Show()
                self.view_panels[i].Layout()
                out = self.view_panels[i]
            else:
                self.view_panels[i].Hide()
        self.Layout()
        return out