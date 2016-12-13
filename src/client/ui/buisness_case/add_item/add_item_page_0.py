import wx

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class AddItemPage0(wx.Panel):
    def __init__(self, 
                 cases_controller, 
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.doLayout()
        self.bind()
        
#----------------------------------------------------------------------------------------------
    def doLayout(self):
        self.split1 = wx.SplitterWindow(self, style = wx.SP_THIN_SASH)
        
        self.lpanel = wx.Panel(self.split1, wx.ID_ANY)
        self.rpanel = wx.Panel(self.split1, wx.ID_ANY)
        
        self.lpanel.SetBackgroundColour((255, 0, 0))
        self.rpanel.SetBackgroundColour((255, 0, 255))
        
        self.split1.SplitVertically(self.lpanel, self.rpanel)
        self.split1.SetSashGravity(0.25)
        self.split1.SetMinimumPaneSize(250)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.split1, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.split1.SetSashPosition(200, True)
        self.Layout()

#----------------------------------------------------------------------------------------------
    def bind(self):
        pass