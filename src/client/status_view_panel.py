import wx

class StatusViewPanel(wx.Panel):
    def __init__(self, specs, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.specs = specs
        self.name = wx.StaticText(self, label="Hello: %s " % self.specs['name'], pos=(10, 10))
        self.name.SetForegroundColour((255, 255, 255))
        self.logoffButton = wx.Button(self, label="Logoff", pos=(700, 10), size=(40, 20))
    
        self.Bind(wx.EVT_BUTTON, self.OnClickLogOff, self.logoffButton)
        
    def OnClickLogOff(self, event):
        print "OnClickLogOff"
        
        self.GetParent().ms_connection.send({'opcode': 'logout'})
        
        #self.GetParent().OnLogOff()
        #self.GetParent().Close(False)
        pass