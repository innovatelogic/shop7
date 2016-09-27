import sys
import wx, wx.html
from proportional_splitter import ProportionalSplitter
import httplib, urllib

TITLE_DLG = "Login Buisness___"

#############################################################################
class AuthHTTPConnection:
    def __init__(self, specs):
        self.specs = specs
        self.url = self.specs['auth']['host'] + ':' + self.specs['auth']['port']
        self.connection = None
        
        self.initConnection()
        
    def initConnection(self):
        self.connection = httplib.HTTPConnection(self.url)

    def stopConnection(self):
        self.connection.close()
        
    def request(self, login, password):
        params = { 'opcode':'auth', 'login': login, 'password': password}

        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        
        self.connection.request("POST", "/", str(params), headers=headers)
        
        res = self.connection.getresponse()
        print res.status, res.reason
        
#############################################################################
class LoginPanel(wx.Panel):
    def __init__(self, connection, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.connection = connection
        self.login = wx.TextCtrl(self, value="", pos=(50, 200), size=(180,-1))
        self.passw = wx.TextCtrl(self, value="", pos=(50, 250), size=(180,-1), style=wx.TE_PASSWORD)
        self.loginButton = wx.Button(self, label="Login", pos=(50, 300), size=(180, -1))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickLogin, self.loginButton)
        self.SetBackgroundColour((250, 178, 54))
    
    def OnClickLogin(self, event):
        self.connection.request(self.login.GetValue(), self.passw.GetValue())
       

#############################################################################
class LoginDialog(wx.Dialog):
    def __init__(self, specs):
        wx.Dialog.__init__(self, None, -1, TITLE_DLG,
            style= (wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.TAB_TRAVERSAL) ^ wx.RESIZE_BORDER,
            size=(800, 600))
        self.specs = specs
        
        self.auth_connection = AuthHTTPConnection(specs)
        
        image = wx.Image('D:/shop7/res/img.jpg', wx.BITMAP_TYPE_ANY)

        leftpanel = LoginPanel(self.auth_connection, self, wx.ID_ANY, size=(280, 600), pos=(0, 0))
        rightpanel = wx.Panel(self, wx.ID_ANY, size = (500, 600), pos = (280, 0))
        
        imageBitmap = wx.StaticBitmap(rightpanel, wx.ID_ANY, wx.BitmapFromImage(image))
        
        leftpanel.SetBackgroundColour((250, 178, 54))
        rightpanel.SetBackgroundColour((0, 178, 54))
        
        self.Fit()

        
        