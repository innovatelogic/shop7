import wx
from groups_tree_view import GroupsTreeView
                
class DocumentViewPanel(wx.Panel):
    def __init__(self, connection_info, ms_connection, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.connection_info = connection_info
        self.ms_connection = ms_connection
        self.SetBackgroundColour((255, 255, 255))
        self.doLayout()
        
    def doLayout(self):
        W,H = self.GetSize()
        self.toppanel = wx.Panel(self, wx.ID_ANY, size = (-1, 45), pos = (0, 0))
        self.toppanel.SetBackgroundColour((215, 0, 215))
        self.bottompanel = wx.Panel(self, wx.ID_ANY)
        self.bottompanel.SetBackgroundColour((255, 255, 255))
        
        posCenterPanelVertSzr = wx.BoxSizer(wx.VERTICAL)
        posCenterPanelVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posCenterPanelVertSzr.Add(self.bottompanel, 1, wx.GROW)
        self.SetSizer(posCenterPanelVertSzr)
                
        self.bottompanel.left_tree = GroupsTreeView(self.ms_connection, self.bottompanel, 1, wx.DefaultPosition, (250, -1),
                                                                 wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT)
        self.bottompanel.right = wx.Panel(self.bottompanel, wx.ID_ANY)
        self.bottompanel.right.SetBackgroundColour((235, 235, 235))
        
        posDocHorSzr = wx.BoxSizer(wx.HORIZONTAL)
        posDocHorSzr.Add(self.bottompanel.left_tree, 0, wx.EXPAND)
        posDocHorSzr.Add(self.bottompanel.right, 1, wx.GROW)
        self.bottompanel.SetSizer(posDocHorSzr)