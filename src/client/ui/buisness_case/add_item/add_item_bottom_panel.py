import wx

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ButtonPanel(wx.Panel):
    BTN_WIDTH = 50
    BTN_HEIGHT = 30
    SHIFT = 10
    
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.buttons = []
        self.doLayout()
        
    def doLayout(self):
        self.prev_button = wx.Button(self, label="<< Prev", pos = (0, 0), size = (self.BTN_WIDTH, self.BTN_HEIGHT))
        self.next_button = wx.Button(self, label="Next >>", pos = (self.BTN_WIDTH + self.SHIFT, 0), size = (self.BTN_WIDTH, self.BTN_HEIGHT))

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class AddItemBottomPanel(wx.Panel):
    def __init__(self, 
                 cases_controller, 
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.doLayout()
        self.bind()
        
#----------------------------------------------------------------------------------------------
    def doLayout(self):
        gridsizer = wx.FlexGridSizer(cols=3, rows = 1)
        gridsizer.AddGrowableRow(0)
        gridsizer.AddGrowableCol(0)

        self.btnpanel = ButtonPanel(self, wx.ID_ANY, pos = (0, 0), size = (120, -1))
        
        sizer_0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_0.Add((20,-1), 1, wx.EXPAND) # this is a spacer

        sizer_1.Add(self.btnpanel, flag = wx.ALIGN_CENTER_VERTICAL)
        sizer_2.Add((100,-1), 1, wx.EXPAND) # this is a spacer
        
        gridsizer.Add(sizer_0, flag = wx.EXPAND) 
        gridsizer.Add(sizer_1, flag = wx.EXPAND) 
        gridsizer.Add(sizer_2, flag = wx.EXPAND)
        
        self.SetSizer(gridsizer)
        self.Layout()
        
#----------------------------------------------------------------------------------------------
    def bind(self):
        self.Bind(wx.EVT_BUTTON, self.OnClick_Prev, self.btnpanel.prev_button)
        self.Bind(wx.EVT_BUTTON, self.OnClick_Next, self.btnpanel.next_button)
        pass
    
#----------------------------------------------------------------------------------------------
    def OnClick_Prev(self, event):
        self.cases_controller.getAddItemController().prevStep()
        
#----------------------------------------------------------------------------------------------
    def OnClick_Next(self, event):
        self.cases_controller.getAddItemController().nextStep()    