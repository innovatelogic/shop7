import wx
from proportional_splitter import ProportionalSplitter
from status_view_panel import StatusViewPanel
from doc_control_panel import DocControlPanel
from document_view_panel import DocumentViewPanel
TITLE_DLG = "Client"
ONLINE_PANEL_HEIGHT = 50
LEFT_PANEL_WIDTH = 100


class EPanels:
    EPanel_Cases = 0
    EPanel_Clients = 1
    EPanel_Connect = 2
    EPanel_Settings = 3
    EPanel_Statistics = 4
    EPanel_Dashboard = 5
    EPanel_MAX = 6

class DocumentFrame(wx.Frame):
    logout_flag = False
    def __init__(self, parent, connection_info, ms_connection):
        wx.Frame.__init__(self, parent, title=TITLE_DLG, size=(800, 600))
        self.connection_info = connection_info
        self.ms_connection = ms_connection
        DocumentFrame.logout_flag = False
        self.view_panels = []
        self.InitInterface()
                
        self.Show(True)
        
    def InitInterface(self):
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")

        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar()
        
        self.doLayout();
        
        self.BindEvents()
        
    def doLayout(self):
        self.toppanel = StatusViewPanel(self.connection_info, self, wx.ID_ANY, size = (self.GetSize().GetWidth(), ONLINE_PANEL_HEIGHT), pos = (0, 0))
        self.toppanel.SetBackgroundColour((34, 65, 96))
        
        self.bottompanel = wx.Panel(self, wx.ID_ANY)
        self.bottompanel.SetBackgroundColour((0, 0, 0))
        
        posVertSzr = wx.BoxSizer(wx.VERTICAL)
        posVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posVertSzr.Add(self.bottompanel, 1, wx.GROW)
        self.SetSizer(posVertSzr)
              
        left_panel_height = self.GetSize().GetHeight() - ONLINE_PANEL_HEIGHT
        self.leftpanel = DocControlPanel(self.connection_info, 
                                         self.bottompanel,
                                         wx.ID_ANY,
                                         size = (LEFT_PANEL_WIDTH, left_panel_height), pos = (0, ONLINE_PANEL_HEIGHT))
        
        center_panel_width = self.GetSize().GetWidth() - LEFT_PANEL_WIDTH
        self.centerpanel = wx.Panel(self.bottompanel, wx.ID_ANY, size = (center_panel_width, left_panel_height),
                                             pos = (LEFT_PANEL_WIDTH, ONLINE_PANEL_HEIGHT))
        
        posHorSzr = wx.BoxSizer(wx.HORIZONTAL)
        posHorSzr.Add(self.leftpanel, 0, wx.EXPAND)
        posHorSzr.Add(self.centerpanel, 1, wx.GROW)
        self.bottompanel.SetSizer(posHorSzr)
        
        # toggle panels
        self.cases_panel = DocumentViewPanel(self.connection_info, self.ms_connection, 
                                             self.centerpanel, wx.ID_ANY, size = (-1, -1))
        self.clients_panel = wx.Panel(self.centerpanel, wx.ID_ANY, size = (center_panel_width, left_panel_height))
        self.connect_panel = wx.Panel(self.centerpanel, wx.ID_ANY, size = (center_panel_width, left_panel_height))
        self.settings_panel = wx.Panel(self.centerpanel, wx.ID_ANY, size = (center_panel_width, left_panel_height))
        self.statistics_panel = wx.Panel(self.centerpanel, wx.ID_ANY, size = (center_panel_width, left_panel_height))
        self.dashboard_panel = wx.Panel(self.centerpanel, wx.ID_ANY, size = (center_panel_width, left_panel_height))
        
        self.view_panels.append(self.cases_panel)
        self.view_panels.append(self.clients_panel)
        self.view_panels.append(self.connect_panel)
        self.view_panels.append(self.settings_panel)
        self.view_panels.append(self.statistics_panel)
        self.view_panels.append(self.dashboard_panel)
        
        self.gridsizer = wx.FlexGridSizer(cols=1, rows = 1)
        self.gridsizer.AddGrowableRow(0)
        self.gridsizer.AddGrowableCol(0)
      
        self.TogglePanel(EPanels.EPanel_Cases)
        
        self.centerpanel.SetSizer(self.gridsizer)
        
        self.Layout()
        #self.cases_panel.Layout()
        
    def OnReSize(self, event):
            "Window has been resized, so we need to adjust the window."
            #self.centerpanel.Layout()
            #W,H = self.centerpanel.GetSize()
            #for i in range(0, EPanels.EPanel_MAX):
            #    self.view_panels[i].SetSize(W, H)
            event.Skip()
            
    def OnLogOff(self):
        self.ms_connection.send_msg('logout', {})
        DocumentFrame.logout_flag = True
        
    def GetGroups(self, id):
        return self.ms_connection.send_msg('get_groups', {'id':id})
    
    def BindEvents(self):
        self.Bind(wx.EVT_SIZE, self.OnReSize)
        self.Bind(wx.EVT_BUTTON, self.OnClick_Cases, self.leftpanel.btn_cases)
        self.Bind(wx.EVT_BUTTON, self.OnClick_Clients, self.leftpanel.btn_clients)
        self.Bind(wx.EVT_BUTTON, self.OnClick_Connect, self.leftpanel.btn_conect)
        self.Bind(wx.EVT_BUTTON, self.OnClick_Settings, self.leftpanel.btn_settings)
        self.Bind(wx.EVT_BUTTON, self.OnClick_Statistics, self.leftpanel.btn_statistics)
        self.Bind(wx.EVT_BUTTON, self.OnClick_Dashboard, self.leftpanel.btn_dashboard)
        
    def TogglePanel(self, index):
        out = None
        self.gridsizer.Clear()
        for i in range(0, EPanels.EPanel_MAX):
            if i == index:
                self.gridsizer.Add(self.view_panels[i], 0, wx.EXPAND)
                self.view_panels[i].Show()
                self.view_panels[i].Layout()
                out = self.view_panels[i]
            else:
                self.view_panels[i].Hide()
        self.centerpanel.Layout()
        return out
        
    def OnClick_Cases(self, event):
        self.TogglePanel(EPanels.EPanel_Cases)
        
    def OnClick_Clients(self, event):
        panel = self.TogglePanel(EPanels.EPanel_Clients)
        panel.SetBackgroundColour((255, 0, 0))
    
    def OnClick_Connect(self, event):
        panel = self.TogglePanel(EPanels.EPanel_Connect)
        panel.SetBackgroundColour((0, 255, 0))
    
    def OnClick_Settings(self, event):
        panel = self.TogglePanel(EPanels.EPanel_Settings)
        panel.SetBackgroundColour((0, 255, 255))
        
    def OnClick_Statistics(self, event):
        panel = self.TogglePanel(EPanels.EPanel_Statistics)
        panel.SetBackgroundColour((0, 123, 255))
        
    def OnClick_Dashboard(self, event):
        panel = self.TogglePanel(EPanels.EPanel_Dashboard)
        panel.SetBackgroundColour((123, 123, 255))