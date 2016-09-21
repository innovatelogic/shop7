import wx
from proportional_splitter import ProportionalSplitter
from groups_tree_view import GroupsTreeView

TITLE_DLG = "Client"

class DocumentFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=TITLE_DLG, size=(800, 600))
        
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        #self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        #self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar()

        self.split1 = ProportionalSplitter(self, wx.ID_ANY, 0.2)
        #self.split2 = ProportionalSplitter(self.split1, wx.ID_ANY, 0.50)
        
        self.tree = GroupsTreeView(self.split1, 1, wx.DefaultPosition, (-1, -1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        
        self.leftpanel = self.tree #wx.Panel(self.split1)
        
        
        #self.leftpanel.Add(self.tree, 1, wx.EXPAND)
        
        #self.leftpanel.SetBackgroundColour('pink')
        
        self.rightpanel = wx.Panel(self.split1)
        self.rightpanel.SetBackgroundColour((200, 191, 231))    
        
        self.split1.SplitVertically(self.leftpanel, self.rightpanel)
        
        #self.topleftpanel = wx.Panel (self.split2)
        #self.topleftpanel.SetBackgroundColour('pink')
        
        
        #self.bottomleftpanel = wx.Panel (self.split2)
        #self.bottomleftpanel.SetBackgroundColour('sky Blue')

        ## add your controls to the splitters:
        #self.split1.SplitVertically(self.split2, self.rightpanel)
        #self.split2.SplitHorizontally(self.topleftpanel, self.bottomleftpanel)
                
        self.Show(True)