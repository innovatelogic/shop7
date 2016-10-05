import wx

class StatusViewPanel(wx.Panel):
    def __init__(self, connection_info, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.connection_info = connection_info
        self.name = wx.StaticText(self, label="Hello: %s " % self.connection_info['name'], pos=(10, 10))
        self.name.SetForegroundColour((255, 255, 255))
        self.logoffButton = wx.Button(self, label="Logoff", pos=(700, 10), size=(40, 20))
    
        self.Bind(wx.EVT_BUTTON, self.OnClickLogOff, self.logoffButton)
        
    def OnClickLogOff(self, event):
        print "OnClickLogOff"
        self.GetParent().OnLogOff()
        self.GetParent().Close(False)
        pass