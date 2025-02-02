import wx
from add_item_top_panel import AddItemTopPanel
from add_item_bottom_panel import AddItemBottomPanel
from add_item_center_panel import AddItemCenterPanel

#----------------------------------------------------------------------------------------------
class AddItemMainPanel(wx.Panel):
    def __init__(self, cases_controller, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.doLayout()
        pass

#----------------------------------------------------------------------------------------------
    def doLayout(self):
        self.toppanel = AddItemTopPanel(self.cases_controller, self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        self.bottompanel = wx.Panel(self, wx.ID_ANY)
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.toppanel, 0, wx.EXPAND)
        vsizer.Add(self.bottompanel, 1, wx.GROW)
        
        self.SetSizer(vsizer)
        self.Layout()
        
        self.child_toppanel = AddItemCenterPanel(self.cases_controller, self.bottompanel, wx.ID_ANY, size=(-1, 25))
        self.child_bottompanel = AddItemBottomPanel(self.cases_controller, self.bottompanel, wx.ID_ANY, size = (-1, 30))
        
        gridsizer = wx.FlexGridSizer(cols=1, rows = 2)
        gridsizer.AddGrowableRow(0)
        gridsizer.AddGrowableCol(0)
        
        gridsizer.Add(self.child_toppanel, flag = wx.ALL|wx.EXPAND)
        gridsizer.Add(self.child_bottompanel, flag = wx.ALL|wx.EXPAND)
        self.bottompanel.SetSizer(gridsizer)
        
        self.bottompanel.Layout()

#----------------------------------------------------------------------------------------------
    def setPage(self, page):
        
        self.child_bottompanel.setPage(page)
        self.child_toppanel.ToggleCenterPage(page)
        
        if page == 0:
            pass
        elif page == 1:
            pass
        elif page == 2:
            pass
        else:
            print('Error')
        print('setPage: {}'.format(page))