import wx
from realm.realm import Realm

class StatusViewPanel(wx.Panel):
    def __init__(self, realm, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = realm
        
        bmp = wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (16, 16))
        inputOneIco = wx.StaticBitmap(self, wx.ID_ANY, bmp)
        inputTxtOne = wx.TextCtrl(self, wx.ID_ANY, '', size=(140, 20))

        self.label_name = wx.StaticText(self, label="Hello: %s " % self.realm.connection_info['name'], pos=(10, 10))
        self.label_name.SetForegroundColour((255, 255, 255))
        self.logoffButton = wx.Button(self, label="Logoff", size=(40, 20))
        
        gridsizer = wx.FlexGridSizer(cols=5, rows = 1)
        gridsizer.AddGrowableRow(0)
        gridsizer.AddGrowableCol(1)
        gridsizer.AddGrowableCol(3)
         
        sizer_0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_0.Add(inputOneIco, flag = wx.ALIGN_CENTER_VERTICAL) 
        sizer_0.Add(self.label_name, flag = wx.ALIGN_CENTER_VERTICAL)
        
        sizer_1.Add((20,20), 1, wx.EXPAND)
        
        sizer_2.Add((20,20), 1, wx.EXPAND) # this is a spacer
        sizer_2.Add(inputTxtOne, flag = wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        sizer_2.Add((20,20), 1, wx.EXPAND) # this is a spacer
        
        sizer_3.Add((20,20), 1, wx.EXPAND)
        
        sizer_4.Add((20,-1), 1, wx.EXPAND) # this is a spacer
        sizer_4.Add(self.logoffButton, flag = wx.ALIGN_CENTER_VERTICAL)
        sizer_4.Add((5,-1), 1, wx.EXPAND)
         
        gridsizer.Add(sizer_0, flag = wx.EXPAND) 
        gridsizer.Add(sizer_1, flag = wx.EXPAND) 
        gridsizer.Add(sizer_2, flag = wx.EXPAND)
        gridsizer.Add(sizer_3, flag = wx.EXPAND)
        gridsizer.Add(sizer_4, flag = wx.EXPAND)

        self.SetSizer(gridsizer)

        self.Bind(wx.EVT_BUTTON, self.OnClickLogOff, self.logoffButton)
        
    def OnClickLogOff(self, event):
        print "OnClickLogOff"
        self.GetParent().OnLogOff()
        self.GetParent().Close(False)
        pass