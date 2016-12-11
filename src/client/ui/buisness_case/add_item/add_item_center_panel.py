import wx

#----------------------------------------------------------------------------------------------
class AddItemCenterPanel(wx.Panel):
    def __init__(self, 
                 cases_controller, 
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.doLayout()
        
    def doLayout(self):
        self.SetBackgroundColour((255, 255, 255))
        pass