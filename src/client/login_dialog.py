import wx

TITLE_DLG = "Login Buisness___"

class LoginPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.login = wx.TextCtrl(self, value="email", pos=(50, 200), size=(180,-1))
        self.passw = wx.TextCtrl(self, value="password", pos=(50, 250), size=(180,-1))
        self.loginButton = wx.Button(self, label="Login", pos=(50, 300), size=(180, -1))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickLogin, self.loginButton)
    
    def OnClickLogin(self, event):
        self.GetParent().Destroy()
        return

class LoginDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, TITLE_DLG,
            style= (wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.TAB_TRAVERSAL) ^ wx.RESIZE_BORDER,
            size=(800, 600))
        
        self.panel_left = LoginPanel(self)

        
        