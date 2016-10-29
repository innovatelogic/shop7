import wx

class ItemsListBottomControlPanel(wx.Panel):
    def __init__(self, connection_info, ms_connection, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.connection_info = connection_info
        self.ms_connection = ms_connection 
        
        self.doLayout()
        
    def doLayout(self):
        bmp_search = wx.Bitmap("../res/img/dropdown.png", wx.BITMAP_TYPE_ANY)
        self.left_btn = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_search, size = (20, 20))
        self.right_btn = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_search, size = (20, 20))
        self.inputTxt = wx.TextCtrl(self, wx.ID_ANY, '', size=(40, 20))
        self.label_count = wx.StaticText(self, label="1/5")
        
        gridsizer = wx.FlexGridSizer(cols=2, rows = 1)
        gridsizer.AddGrowableCol(0)
        
        sizer_0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_0.Add((40,-1), 1, wx.EXPAND) # this is a spacer
        
        sizer_1.Add(self.left_btn, flag = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer_1.Add(self.inputTxt, flag = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer_1.Add(self.right_btn, flag = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer_1.Add(self.label_count, flag = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer_1.Add((50,-1), 1, wx.EXPAND) # this is a spacer
        
        gridsizer.Add(sizer_0, flag = wx.EXPAND) 
        gridsizer.Add(sizer_1, flag = wx.EXPAND) 
        
        self.SetSizer(gridsizer)
        
        self.Layout()