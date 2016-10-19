import wx

class StatusViewPanel(wx.Panel):
    def __init__(self, connection_info, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.connection_info = connection_info
        
        bmp = wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (16, 16))
        inputOneIco = wx.StaticBitmap(self, wx.ID_ANY, bmp)
        inputTxtOne = wx.TextCtrl(self, wx.ID_ANY, '', size=(140, 20))

        self.label_name = wx.StaticText(self, label="Hello: %s " % self.connection_info['name'], pos=(10, 10))
        self.label_name.SetForegroundColour((255, 255, 255))
        self.logoffButton = wx.Button(self, label="Logoff", size=(40, 20))
        
        #topSizer = wx.BoxSizer(wx.HORIZONTAL)
        #gridSizer = wx.GridSizer(rows=1, cols=3, hgap=5, vgap=5)
        
        gridsizer = wx.FlexGridSizer(cols=5, rows = 1)
        gridsizer.AddGrowableRow(0)
        gridsizer.AddGrowableCol(1)
        gridsizer.AddGrowableCol(3)
        
        #sizer_vert  = wx.BoxSizer(wx.VERTICAL)
        #sizer_hor_1 = wx.BoxSizer(wx.HORIZONTAL)
        
        #sizer_vert.Add (sizer_hor_1)
         
        sizer_0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        
        #inputOneSizer.Add((20,-1), 1, wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)  # this is a spacer
        
        sizer_0.Add(inputOneIco, flag = wx.ALIGN_CENTER_VERTICAL) #, 1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5
        sizer_0.Add(self.label_name, flag = wx.ALIGN_CENTER_VERTICAL) #, 1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5
        
        sizer_1.Add((20,20), 1, wx.EXPAND)
        
        #inputTwoSizer.Add((20,20), 1, wx.EXPAND) # this is a spacer
        sizer_2.Add((20,20), 1, wx.EXPAND) # this is a spacer
        sizer_2.Add(inputTxtOne, flag = wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        sizer_2.Add((20,20), 1, wx.EXPAND) # this is a spacer
        #inputTwoSizer.Add(labelTwo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        sizer_3.Add((20,20), 1, wx.EXPAND)
        
        sizer_4.Add((20,-1), 1, wx.EXPAND) # this is a spacer
        sizer_4.Add(self.logoffButton, flag = wx.ALIGN_CENTER_VERTICAL)
        sizer_4.Add((5,-1), 1, wx.EXPAND)
         
        gridsizer.Add(sizer_0, flag = wx.EXPAND) #, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5
        gridsizer.Add(sizer_1, flag = wx.EXPAND) #, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL
        gridsizer.Add(sizer_2, flag = wx.EXPAND)
        gridsizer.Add(sizer_3, flag = wx.EXPAND)
        gridsizer.Add(sizer_4, flag = wx.EXPAND) #, 0, , flag = wx.ALIGN_CENTER_VERTICAL
        
        
        #self.Add(gridSizer, 0, wx.ALL|wx.EXPAND, 5)
        #parentsizer.Add (sizer_hor_1, flag = wx.EXPAND)
        self.SetSizer(gridsizer)
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