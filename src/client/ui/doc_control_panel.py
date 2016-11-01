import wx
import wx.lib.agw.gradientbutton as GB
                
class DocControlPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.SetBackgroundColour((34, 65, 96))
        
        self.doLayout()
        
    def doLayout(self):
        gridsizer = wx.FlexGridSizer(cols=1, rows = 8)
        gridsizer.AddGrowableRow(7)
        gridsizer.AddGrowableCol(0)
        
        bmp_folder = wx.Bitmap("../res/folder.png", wx.BITMAP_TYPE_ANY)
        bmp_gear = wx.Bitmap("../res/gear.png", wx.BITMAP_TYPE_ANY)
        bmp_clients = wx.Bitmap("../res/people.png", wx.BITMAP_TYPE_ANY)
        bmp_conect = wx.Bitmap("../res/connect.png", wx.BITMAP_TYPE_ANY)
        bmp_statistics = wx.Bitmap("../res/img/statistics.png", wx.BITMAP_TYPE_ANY)
        bmp_dashboard = wx.Bitmap("../res/img/dashboard.png", wx.BITMAP_TYPE_ANY)
        
        self.btn_cases = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_folder, size = (-1, 70))
        self.btn_cases.SetBackgroundColour((34, 65, 96))
        self.btn_cases.SetForegroundColour((255, 255, 255))
        self.btn_cases.SetWindowStyleFlag(wx.NO_BORDER)

        self.btn_clients = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_clients, size = (-1, 70))
        self.btn_clients.SetBackgroundColour((34, 65, 96))
        self.btn_clients.SetForegroundColour((255, 255, 255))
        self.btn_clients.SetWindowStyleFlag(wx.NO_BORDER)
        
        self.btn_conect = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_conect, size = (-1, 70))
        self.btn_conect.SetBackgroundColour((34, 65, 96))
        self.btn_conect.SetForegroundColour((255, 255, 255))
        self.btn_conect.SetWindowStyleFlag(wx.NO_BORDER)
        
        self.btn_settings = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_gear, size = (-1, 70))
        self.btn_settings.SetBackgroundColour((34, 65, 96))
        self.btn_settings.SetForegroundColour((255, 255, 255))
        self.btn_settings.SetWindowStyleFlag(wx.NO_BORDER)
        
        self.btn_statistics = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_statistics, size = (-1, 70))
        self.btn_statistics.SetBackgroundColour((34, 65, 96))
        self.btn_statistics.SetForegroundColour((255, 255, 255))
        self.btn_statistics.SetWindowStyleFlag(wx.NO_BORDER)
        
        self.btn_dashboard = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_dashboard, size = (-1, 70))
        self.btn_dashboard.SetBackgroundColour((34, 65, 96))
        self.btn_dashboard.SetForegroundColour((255, 255, 255))
        self.btn_dashboard.SetWindowStyleFlag(wx.NO_BORDER)
        
        gridsizer.Add((-1,45), 0, wx.EXPAND)
        gridsizer.Add(self.btn_cases, flag = wx.BOTTOM|wx.EXPAND, border = 4)
        gridsizer.Add(self.btn_clients, flag = wx.BOTTOM|wx.EXPAND, border = 4)
        gridsizer.Add(self.btn_conect, flag = wx.BOTTOM|wx.EXPAND, border = 4)
        gridsizer.Add(self.btn_settings, flag = wx.BOTTOM|wx.EXPAND, border = 4)
        gridsizer.Add(self.btn_statistics, flag = wx.BOTTOM|wx.EXPAND, border = 4)
        gridsizer.Add(self.btn_dashboard, flag = wx.BOTTOM|wx.EXPAND, border = 4)
        gridsizer.Add((20,20), 1, wx.EXPAND)
        
        self.SetSizer(gridsizer)
        pass