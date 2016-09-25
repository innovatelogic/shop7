import sys
import wx, wx.html
from proportional_splitter import ProportionalSplitter
import httplib, urllib

TITLE_DLG = "Login Buisness___"

aboutText = """<p>Sorry, there is no information about this program. It is
14 running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.
15 See <a href="http://wiki.wxpython.org">wxPython Wiki</a></p>""" 

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

class LoginPanel(wx.Panel):
    def __init__(self, specs, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.specs = specs
        self.login = wx.TextCtrl(self, value="", pos=(50, 200), size=(180,-1))
        self.passw = wx.TextCtrl(self, value="", pos=(50, 250), size=(180,-1), style=wx.TE_PASSWORD)
        self.loginButton = wx.Button(self, label="Login", pos=(50, 300), size=(180, -1))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickLogin, self.loginButton)
        self.SetBackgroundColour((250, 178, 54))
    
    def OnClickLogin(self, event):
        #self.GetParent().Destroy()
        conn = httplib.HTTPConnection(self.specs['auth']['host'] + ':' + self.specs['auth']['port'])
        
        params = urllib.urlencode({'login': self.login.GetValue(), 'pass': self.passw.GetValue()})
      
        conn.request("POST", params)
        res = conn.getresponse()
        print res.status, res.reason
        
        conn.close()


class LoginDialog(wx.Dialog):
    def __init__(self, specs):
        wx.Dialog.__init__(self, None, -1, TITLE_DLG,
            style= (wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.TAB_TRAVERSAL) ^ wx.RESIZE_BORDER,
            size=(800, 600))
        self.specs = specs
        
        #self.split1 = ProportionalSplitter(self, wx.ID_ANY, 0.4)
        #self.split1.SetSashInvisible(False)    

        ##self.leftpanel = wx.Panel(self.split1)
        
        #self.leftpanel = LoginPanel(self.split1)
        #self.rightpanel = wx.Panel(self.split1)
        #self.rightpanel.SetBackgroundColour((200, 191, 231))    
        
        #self.split1.SplitVertically(self.leftpanel, self.rightpanel)
        
        #self.mgr = wx.aui.AuiManager(self)
        
        image = wx.Image('D:/shop7/res/img.jpg', wx.BITMAP_TYPE_ANY)
        #self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))

        leftpanel = LoginPanel(self.specs, self, wx.ID_ANY, size=(280, 600), pos=(0, 0))
        rightpanel = wx.Panel(self, wx.ID_ANY, size = (500, 600), pos = (280, 0))
        
        imageBitmap = wx.StaticBitmap(rightpanel, wx.ID_ANY, wx.BitmapFromImage(image))

        
        leftpanel.SetBackgroundColour((250, 178, 54))
        rightpanel.SetBackgroundColour((0, 178, 54))
        #bottompanel = wx.Panel(self, -1, size = (200, 150))

        #self.mgr.AddPane(leftpanel, wx.aui.AuiPaneInfo().Left().Position(0).CloseButton(False))
        #self.mgr.AddPane(rightpanel, wx.aui.AuiPaneInfo().Right().Position(1).
        #                 MinSize(rightpanel.GetBestSize()).BestSize(rightpanel.GetBestSize()).CloseButton(False))
        #self.mgr.AddPane(bottompanel, wx.aui.AuiPaneInfo().Center().Layer(2))

        #self.mgr.Update()
        
        self.Fit()
        
        #hwin = HtmlWindow(self, -1, size=(400,200))
        #vers = {}
        #vers["python"] = sys.version.split()[0]
        #vers["wxpy"] = wx.VERSION_STRING
        #hwin.SetPage(aboutText % vers)
        #self.panel_left = LoginPanel(self, size=(500, 600))

        
        