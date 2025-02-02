import sys
import wx, wx.html
from proportional_splitter import ProportionalSplitter
from connections.auth_http_connection import AuthHTTPConnection

TITLE_DLG = "Login Buisness___"
        
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class LoginPanel(wx.Panel):
    X_POS = 50
    SIZE_DEF=(180,-1)
    
    def __init__(self, connection, specs, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.specs = specs
        self.auth_connection = connection
        self.login = wx.TextCtrl(self, value=self.specs['user']['login'], pos=(self.X_POS, 200), size=self.SIZE_DEF)
        self.passw = wx.TextCtrl(self, value=self.specs['user']['pass'], pos=(self.X_POS, 250), size=self.SIZE_DEF, style=wx.TE_PASSWORD)
        self.anon = wx.CheckBox(self, label = 'login anonymous', pos=(self.X_POS, 285), size=self.SIZE_DEF)
        self.loginButton = wx.Button(self, label="Login", pos=(self.X_POS, 310), size=self.SIZE_DEF)
        
        self.Bind(wx.EVT_BUTTON, self.OnClickLogin, self.loginButton)
        self.SetBackgroundColour((250, 178, 54))
        
        self.Bind(wx.EVT_CHECKBOX, self.onAnonChecked, self.anon) 
    
    def OnClickLogin(self, event):
        res, options = self.auth_connection.request(self.login.GetValue(), self.passw.GetValue(), self.anon.GetValue())
        if res:
            self.GetParent().connection_info = options
            self.GetParent().Close(False)
       
    def onAnonChecked(self, e): 
        cb = e.GetEventObject()
        enable = cb.GetValue() == False
        self.login.Enable(enable)
        self.passw.Enable(enable)
      
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class LoginDialog(wx.Dialog):
    def __init__(self, specs):
        wx.Dialog.__init__(self, None, -1, TITLE_DLG,
            style= (wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.TAB_TRAVERSAL) ^ wx.RESIZE_BORDER,
            size=(800, 600))
        
        self.specs = specs
        self.auth_connection = AuthHTTPConnection(self.specs)
        self.connection_info = ''
        self.on_close = False
        
        image = wx.Image('../res/img.jpg', wx.BITMAP_TYPE_ANY)

        leftpanel = LoginPanel(self.auth_connection, specs, self, wx.ID_ANY, size=(280, 600), pos=(0, 0))
        rightpanel = wx.Panel(self, wx.ID_ANY, size = (500, 600), pos = (280, 0))
        
        imageBitmap = wx.StaticBitmap(rightpanel, wx.ID_ANY, wx.BitmapFromImage(image))
        
        leftpanel.SetBackgroundColour((250, 178, 54))
        rightpanel.SetBackgroundColour((0, 178, 54))
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Fit()
        self.Centre() 
    
    def OnClose(self, event):
        #print('In OnClose')
        self.auth_connection.stopConnection()
        self.on_close = True
        event.Skip()
