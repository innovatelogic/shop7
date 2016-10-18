import wx
from proportional_splitter import ProportionalSplitter
from groups_tree_view import GroupsTreeView
from status_view_panel import StatusViewPanel


TITLE_DLG = "Client"
ONLINE_PANEL_HEIGHT = 50
LEFT_PANEL_WIDTH = 100

class DocumentFrame(wx.Frame):
    logout_flag = False
    def __init__(self, parent, connection_info, ms_connection):
        wx.Frame.__init__(self, parent, title=TITLE_DLG, size=(800, 600))
        self.connection_info = connection_info
        self.ms_connection = ms_connection
        
        DocumentFrame.logout_flag = False
        
        self.InitInterface()
                
        self.Show(True)
        
    def InitInterface(self):
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
        
        self.toppanel = StatusViewPanel(self.connection_info, self, wx.ID_ANY, size = (self.GetSize().GetWidth(), ONLINE_PANEL_HEIGHT), pos = (0, 0))
        self.toppanel.SetBackgroundColour((34, 65, 96))
        
        self.bottompanel = wx.Panel(self, wx.ID_ANY)
        self.bottompanel.SetBackgroundColour((0, 0, 0))
        
        posVertSzr = wx.BoxSizer(wx.VERTICAL)
        posVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posVertSzr.Add(self.bottompanel, 1, wx.GROW)
        self.SetSizer(posVertSzr)
              
        left_panel_height = self.GetSize().GetHeight() - ONLINE_PANEL_HEIGHT
        self.leftpanel = wx.Panel(self.bottompanel, wx.ID_ANY, size = (LEFT_PANEL_WIDTH, left_panel_height), pos = (0, ONLINE_PANEL_HEIGHT))
        self.leftpanel.SetBackgroundColour((34, 65, 96))
        
        center_panel_width = self.GetSize().GetWidth() - LEFT_PANEL_WIDTH
        self.centerpanel = wx.Panel(self.bottompanel, wx.ID_ANY, size = (center_panel_width, left_panel_height), pos = (LEFT_PANEL_WIDTH, ONLINE_PANEL_HEIGHT))
        self.centerpanel.SetBackgroundColour((255, 255, 255))
        
        posHorSzr = wx.BoxSizer(wx.HORIZONTAL)
        posHorSzr.Add(self.leftpanel, 0, wx.EXPAND)
        posHorSzr.Add(self.centerpanel, 1, wx.GROW)
        self.bottompanel.SetSizer(posHorSzr)
        
        ###
        self.centerpanel.toppanel = wx.Panel(self.centerpanel, wx.ID_ANY, size = (center_panel_width, 45), pos = (0, 0))
        self.centerpanel.toppanel.SetBackgroundColour((215, 215, 215))
        self.centerpanel.bottompanel = wx.Panel(self.centerpanel, wx.ID_ANY)
        self.centerpanel.bottompanel.SetBackgroundColour((255, 255, 255))
        
        posCenterPanelVertSzr = wx.BoxSizer(wx.VERTICAL)
        posCenterPanelVertSzr.Add(self.centerpanel.toppanel, 0, wx.EXPAND)
        posCenterPanelVertSzr.Add(self.centerpanel.bottompanel, 1, wx.GROW)
        self.centerpanel.SetSizer(posCenterPanelVertSzr)
                
        self.centerpanel.bottompanel.left_tree = GroupsTreeView(self.ms_connection, self.centerpanel.bottompanel, 1, wx.DefaultPosition, (250, -1),
                                                                 wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT)
        self.centerpanel.bottompanel.right = wx.Panel(self.centerpanel.bottompanel, wx.ID_ANY)
        self.centerpanel.bottompanel.right.SetBackgroundColour((235, 235, 235))
        
        posDocHorSzr = wx.BoxSizer(wx.HORIZONTAL)
        posDocHorSzr.Add(self.centerpanel.bottompanel.left_tree, 0, wx.EXPAND)
        posDocHorSzr.Add(self.centerpanel.bottompanel.right, 1, wx.GROW)
        self.centerpanel.bottompanel.SetSizer(posDocHorSzr)
        
        self.Bind(wx.EVT_SIZE, self.OnReSize)
        
    def OnReSize(self, event):
            "Window has been resized, so we need to adjust the window."
            #self.toppanel.SetSize((self.GetSize().GetWidth(), ONLINE_PANEL_HEIGHT))
            #left_panel_height = self.GetSize().GetHeight() - ONLINE_PANEL_HEIGHT
            #self.leftpanel.SetSize((LEFT_PANEL_WIDTH, left_panel_height))
            #center_panel_width = self.GetSize().GetWidth() - LEFT_PANEL_WIDTH
            #self.centerpanel.SetSize((center_panel_width, left_panel_height))
            event.Skip()
            
    def OnLogOff(self):
        self.ms_connection.send(str({'opcode': 'logout', 'token':self.connection_info['token']}))
        DocumentFrame.logout_flag = True
        
    def GetGroups(self, id):
        return self.ms_connection.send({'opcode': 'get_groups', 'id':id, 'token':self.connection_info['token']})