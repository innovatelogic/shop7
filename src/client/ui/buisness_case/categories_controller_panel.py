import wx
import wx.lib.agw.gradientbutton as GB
from category_trees_panel import EPanelCategory

class ButtonPanel(wx.Panel):

    COLOR_DARK_BLUE_THEME = wx.Colour(34, 65, 96)
    COLOR_LIGHT_GRAY_THEME = wx.Colour(215, 215, 215)
    
    BTN_WIDTH = 70
    BTN_HEIGHT = 35
    BTN_POS_X = 12
    
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.buttons = []
        self.doLayout()
        
        self.ToggleUp(self.base_aspect_button)
        
    def doLayout(self):
        self.base_aspect_button = GB.GradientButton(self, label="My aspect", pos = (0, self.BTN_POS_X), size = (self.BTN_WIDTH, self.BTN_HEIGHT))
        self.second_aspect_button = GB.GradientButton(self, label="Prom", pos = (self.BTN_WIDTH, self.BTN_POS_X), size = (self.BTN_WIDTH, self.BTN_HEIGHT))

        self.base_aspect_button.SetBaseColours(self.COLOR_DARK_BLUE_THEME, self.COLOR_LIGHT_GRAY_THEME)
        self.second_aspect_button.SetBaseColours(self.COLOR_DARK_BLUE_THEME, self.COLOR_LIGHT_GRAY_THEME)
        
        self.base_aspect_button.SetBottomStartColour(self.COLOR_DARK_BLUE_THEME)
        self.second_aspect_button.SetBottomStartColour(self.COLOR_DARK_BLUE_THEME)
        
        self.buttons.append(self.base_aspect_button)
        self.buttons.append(self.second_aspect_button)
        
    def ToggleUp(self, btn):
        for i in range(0, len(self.buttons)):
            pos = self.buttons[i].GetPosition()
            if self.buttons[i] == btn:
                self.buttons[i].Move((pos[0], self.BTN_POS_X - 2))
            else:
                self.buttons[i].Move((pos[0], self.BTN_POS_X))
        
class CategoriesControllerPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.doLayout()
        self.BindEvents()
        
    def doLayout(self):
        gridsizer = wx.FlexGridSizer(cols=2, rows = 1)
        gridsizer.AddGrowableRow(0)
        gridsizer.AddGrowableCol(1)
        
        sizer_0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btnpanel = ButtonPanel(self, wx.ID_ANY, pos = (0, 0), size = (140, -1))
        
        bmp_folder = wx.Bitmap("../res/img/dropdown.png", wx.BITMAP_TYPE_ANY)
        self.dropdown_btn = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_folder, size = (20, 20))

        sizer_0.Add(self.btnpanel, flag = wx.ALL)
        sizer_1.Add((20,-1), 1, wx.EXPAND) # this is a spacer
        sizer_1.Add(self.dropdown_btn, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        
        gridsizer.Add(sizer_0, flag = wx.EXPAND) 
        gridsizer.Add(sizer_1, flag = wx.EXPAND) 

        self.SetSizer(gridsizer)
        
    def BindEvents(self):
        self.Bind(wx.EVT_BUTTON, self.OnClick_BaseAspect, self.btnpanel.base_aspect_button)
        self.Bind(wx.EVT_BUTTON, self.OnClick_SecondAspect, self.btnpanel.second_aspect_button)
        
    def OnClick_BaseAspect(self, event):
        self.btnpanel.ToggleUp(self.btnpanel.base_aspect_button)
        self.GetParent().SwitchPanel(EPanelCategory.EPanel_Base)
    
    def OnClick_SecondAspect(self, event):
        self.btnpanel.ToggleUp(self.btnpanel.second_aspect_button)
        self.GetParent().SwitchPanel(EPanelCategory.EPanel_Secondary)