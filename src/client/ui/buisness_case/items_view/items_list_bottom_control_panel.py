import wx
from wx.lib.masked import NumCtrl
from wx.lib.intctrl import IntCtrl
import wx.lib.intctrl
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemsListBottomControlPanel(wx.Panel):
    ICON_LEFT = "../res/img/left.png"
    ICON_RIGHT = "../res/img/right.png"
    PAGE_OF_FORMAT = " of {}"
    def __init__(self, 
                 cases_controller,
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.doLayout()
        self.bind()
        
#----------------------------------------------------------------------------------------------
    def doLayout(self):
        bmp_left = wx.Bitmap(self.ICON_LEFT, wx.BITMAP_TYPE_ANY)
        bmp_right = wx.Bitmap(self.ICON_RIGHT, wx.BITMAP_TYPE_ANY)
        self.left_btn = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_left, size = (20, 20))
        self.right_btn = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_right, size = (20, 20))
        self.inputTxt = IntCtrl(self, wx.ID_ANY, size=(40, 20))
        self.label_count = wx.StaticText(self, label="")
        
        gridsizer = wx.FlexGridSizer(cols=2, rows = 1)
        gridsizer.AddGrowableCol(0)
        
        sizer_0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_0.Add((40,-1), 1, wx.EXPAND) # this is a spacer
        
        sizer_1.Add(self.left_btn, flag = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer_1.Add(self.inputTxt, flag = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer_1.Add(self.right_btn, flag = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer_1.Add(self.label_count, flag = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer_1.Add((50,-1), 1, wx.EXPAND) # this is a spacer
        
        gridsizer.Add(sizer_0, flag = wx.EXPAND) 
        gridsizer.Add(sizer_1, flag = wx.EXPAND) 
        
        self.SetSizer(gridsizer)
        self.Layout()
        
#----------------------------------------------------------------------------------------------
    def bind(self):
        self.Bind(wx.EVT_BUTTON, self.OnClick_PageInc, self.right_btn)
        self.Bind(wx.EVT_BUTTON, self.OnClick_PageDec, self.left_btn)
        #self.inputTxt.Bind(wx.EVT_TEXT_ENTER, self.onAction)
        pass
    
#----------------------------------------------------------------------------------------------
    def initController(self, state):
        START_PAGE = 1
        self.inputTxt.SetBounds(START_PAGE, state.getPageCount())
        self.updateController(state)
        
#----------------------------------------------------------------------------------------------
    def updateController(self, state):
        self.label_count.SetLabel(self.PAGE_OF_FORMAT.format(state.getPageCount()))
        self.inputTxt.SetValue(state.getCurrPage())
        pass
    
#----------------------------------------------------------------------------------------------
    def OnClick_PageInc(self, event):
        self.cases_controller.page_inc()
        
#----------------------------------------------------------------------------------------------
    def OnClick_PageDec(self, event):
        self.cases_controller.page_dec()
