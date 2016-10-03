import sys
import wx, wx.html
from proportional_splitter import ProportionalSplitter
from auth_http_connection import AuthHTTPConnection

TITLE_DLG = "Login Buisness___"
        
#############################################################################
class LoginPanel(wx.Panel):
    def __init__(self, connection, specs, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.specs = specs
        self.connection = connection
        self.login = wx.TextCtrl(self, value=self.specs['user']['login'], pos=(50, 200), size=(180,-1))
        self.passw = wx.TextCtrl(self, value=self.specs['user']['pass'], pos=(50, 250), size=(180,-1), style=wx.TE_PASSWORD)
        self.loginButton = wx.Button(self, label="Login", pos=(50, 300), size=(180, -1))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickLogin, self.loginButton)
        self.SetBackgroundColour((250, 178, 54))
    
    def OnClickLogin(self, event):
        res, options = self.connection.request(self.login.GetValue(), self.passw.GetValue())
        
        if res:
            self.GetParent().connection_info = options
            self.GetParent().Close(False)
       

#############################################################################
class LoginDialog(wx.Dialog):
    def __init__(self, specs):
        wx.Dialog.__init__(self, None, -1, TITLE_DLG,
            style= (wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.TAB_TRAVERSAL) ^ wx.RESIZE_BORDER,
            size=(800, 600))
        
        self.specs = specs
        self.auth_connection = AuthHTTPConnection(self.specs)
        self.connection_info = ''
        self.on_close = False
        
        image = wx.Image('D:/shop7/res/img.jpg', wx.BITMAP_TYPE_ANY)

        leftpanel = LoginPanel(self.auth_connection, specs, self, wx.ID_ANY, size=(280, 600), pos=(0, 0))
        rightpanel = wx.Panel(self, wx.ID_ANY, size = (500, 600), pos = (280, 0))
        
        imageBitmap = wx.StaticBitmap(rightpanel, wx.ID_ANY, wx.BitmapFromImage(image))
        
        leftpanel.SetBackgroundColour((250, 178, 54))
        rightpanel.SetBackgroundColour((0, 178, 54))
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Fit()
    
    def OnClose(self, event):
        #print('In OnClose')
        self.auth_connection.stopConnection()
        self.on_close = True
        event.Skip()
        pass
