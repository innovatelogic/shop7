import wx

class StatusViewPanel(wx.Panel):
    def __init__(self, connection_info, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.connection_info = connection_info
        
        bmp = wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (16, 16))
        inputOneIco = wx.StaticBitmap(self, wx.ID_ANY, bmp)
        inputTxtOne = wx.TextCtrl(self, wx.ID_ANY, '')

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        gridSizer = wx.GridSizer(rows=1, cols=3, hgap=5, vgap=5)
        
        inputOneSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputTwoSizer = wx.BoxSizer(wx.HORIZONTAL)
        input_3_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.label_name = wx.StaticText(self, label="Hello: %s " % self.connection_info['name'], pos=(10, 10))
        self.label_name.SetForegroundColour((255, 255, 255))
        self.logoffButton = wx.Button(self, label="Logoff", size=(40, 20))
        
        #inputOneSizer.Add((20,-1), proportion=1)  # this is a spacer
        #inputOneSizer.Add(inputOneIco, 1, wx.ALIGN_LEFT, 5)
        inputOneSizer.Add(self.label_name, 1, wx.ALIGN_LEFT, 5)
        
        inputTwoSizer.Add((20,20), 1, wx.EXPAND) # this is a spacer
        inputTwoSizer.Add(inputTxtOne, 1, wx.ALL, 5)
        #inputTwoSizer.Add(labelTwo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        input_3_Sizer.Add((20,20), 1, wx.EXPAND) # this is a spacer
        input_3_Sizer.Add(self.logoffButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        input_3_Sizer.Add((20,20), 1, wx.EXPAND)
         
        gridSizer.Add(inputOneSizer, 0, wx.ALIGN_LEFT)
        gridSizer.Add(inputTwoSizer, 0, wx.EXPAND )
        gridSizer.Add(input_3_Sizer, 0, wx.ALIGN_RIGHT)
        
        
        #self.Add(gridSizer, 0, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer(gridSizer)
        #topSizer.Fit(self)
        
        #self.lpanel = wx.Panel(self, wx.ID_ANY)
        #self.lpanel.SetBackgroundColour((0, 0, 0))
        
        #self.rpanel = wx.Panel(self, wx.ID_ANY)
        #self.rpanel.SetBackgroundColour((255, 0, 0))
        
        #sizer = wx.BoxSizer(wx.HORIZONTAL)
        #sizer.Add(self.lpanel, 1) #<< Note the extra parameter
        #sizer.Add(self.rpanel, 2) #<< Note the extra parameter
        
        #self.connection_info = connection_info
        #self.name = wx.StaticText(self, label="Hello: %s " % self.connection_info['name'], pos=(10, 10))
        #self.name.SetForegroundColour((255, 255, 255))
        #self.logoffButton = wx.Button(self, label="Logoff", pos=(700, 10), size=(40, 20))
    
        self.Bind(wx.EVT_BUTTON, self.OnClickLogOff, self.logoffButton)
        
    def OnClickLogOff(self, event):
        print "OnClickLogOff"
        self.GetParent().OnLogOff()
        self.GetParent().Close(False)
        pass