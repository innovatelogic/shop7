import wx
import wx.lib.agw.gradientbutton as GB
                
class DocControlPanel(wx.Panel):
    def __init__(self, connection_info, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.SetBackgroundColour((34, 65, 96))
        
        self.doLayout()
        
    def doLayout(self):
        gridsizer = wx.FlexGridSizer(cols=1, rows = 6)
        gridsizer.AddGrowableRow(5)
        gridsizer.AddGrowableCol(0)
        
        bmp_folder = wx.Bitmap("../res/folder.png", wx.BITMAP_TYPE_ANY)
        bmp_gear = wx.Bitmap("../res/gear.png", wx.BITMAP_TYPE_ANY)
        bmp_clients = wx.Bitmap("../res/people.png", wx.BITMAP_TYPE_ANY)
        bmp_conect = wx.Bitmap("../res/connect.png", wx.BITMAP_TYPE_ANY)
        
        btn_cases = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_folder, size = (-1, 70))
        btn_cases.SetBackgroundColour((34, 65, 96))
        btn_cases.SetForegroundColour((255, 255, 255))
        btn_cases.SetWindowStyleFlag(wx.NO_BORDER)

        btn_clients = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_clients, size = (-1, 70))
        btn_clients.SetBackgroundColour((34, 65, 96))
        btn_clients.SetForegroundColour((255, 255, 255))
        btn_clients.SetWindowStyleFlag(wx.NO_BORDER)
        
        btn_conect = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_conect, size = (-1, 70))
        btn_conect.SetBackgroundColour((34, 65, 96))
        btn_conect.SetForegroundColour((255, 255, 255))
        btn_conect.SetWindowStyleFlag(wx.NO_BORDER)
        
        btn_settings = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_gear, size = (-1, 70))
        btn_settings.SetBackgroundColour((34, 65, 96))
        btn_settings.SetForegroundColour((255, 255, 255))
        btn_settings.SetWindowStyleFlag(wx.NO_BORDER)
        
        gridsizer.Add((-1,45), 0, wx.EXPAND)
        gridsizer.Add(btn_cases, flag = wx.BOTTOM|wx.EXPAND, border = 4)
        gridsizer.Add(btn_clients, flag = wx.BOTTOM|wx.EXPAND, border = 4)
        gridsizer.Add(btn_conect, flag = wx.BOTTOM|wx.EXPAND, border = 4)
        gridsizer.Add(btn_settings, flag = wx.BOTTOM|wx.EXPAND, border = 4)
        gridsizer.Add((20,20), 1, wx.EXPAND)
        
        self.SetSizer(gridsizer)
        pass