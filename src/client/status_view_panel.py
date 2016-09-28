import wx

class StatusViewPanel(wx.Panel):
    def __init__(self, specs, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.specs = specs
        self.quote = wx.StaticText(self, label="Hello: %s " % self.specs['name'], pos=(20, 30))
