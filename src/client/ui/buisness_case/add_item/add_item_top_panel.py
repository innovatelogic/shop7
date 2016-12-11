import wx
import wx.lib.agw.gradientbutton as GB

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ButtonPanel(wx.Panel):
    BTN_WIDTH = 40
    BTN_HEIGHT = 30
    SHIFT = 5
    
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.buttons = []
        self.doLayout()
        
    def doLayout(self):
        self.cancel_button = wx.Button(self, label="Cancel", pos = (0, 0), size = (self.BTN_WIDTH, self.BTN_HEIGHT))    

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class AddItemTopPanel(wx.Panel):
    def __init__(self, 
                 cases_controller, 
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.realm = cases_controller.realm()
        self.doLayout()

#----------------------------------------------------------------------------------------------
    def doLayout(self):
        gridsizer = wx.FlexGridSizer(cols=3, rows = 1)
        gridsizer.AddGrowableRow(0)
        gridsizer.AddGrowableCol(0)

        self.btnpanel = ButtonPanel(self, wx.ID_ANY, pos = (0, 0), size = (40, -1))
        
        sizer_0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_0.Add((20,-1), 1, wx.EXPAND) # this is a spacer

        sizer_1.Add(self.btnpanel, flag = wx.ALIGN_CENTER_VERTICAL)
        sizer_2.Add((10,-1), 1, wx.EXPAND) # this is a spacer
        
        gridsizer.Add(sizer_0, flag = wx.EXPAND) 
        gridsizer.Add(sizer_1, flag = wx.EXPAND) 
        gridsizer.Add(sizer_2, flag = wx.EXPAND)
        
        self.SetSizer(gridsizer)
        self.Layout()