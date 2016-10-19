import wx
                
class DocumentViewPanel(wx.Panel):
 def __init__(self, connection_info, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)