import wx
from wx.lib.masked import NumCtrl
from wx.lib.intctrl import IntCtrl
import wx.lib.intctrl
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemsListBottomControlPanel(wx.Panel):
    def __init__(self, realm,
                 callback_page_inc,
                 callback_page_dec,
                 callback_page_select,
                parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = realm
        self.callback_page_inc = callback_page_inc
        self.callback_page_dec = callback_page_dec
        self.callback_page_select = callback_page_select
        self.doLayout()
        self.bind()
        
#----------------------------------------------------------------------------------------------
    def doLayout(self):
        bmp_left = wx.Bitmap("../res/img/left.png", wx.BITMAP_TYPE_ANY)
        bmp_right = wx.Bitmap("../res/img/right.png", wx.BITMAP_TYPE_ANY)
        self.left_btn = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_left, size = (20, 20))
        self.right_btn = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_right, size = (20, 20))
        self.inputTxt = IntCtrl(self, wx.ID_ANY, size=(40, 20))
        self.label_count = wx.StaticText(self, label="1/5")
        
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
    def OnClick_PageInc(self, event):
        self.callback_page_inc()
        
#----------------------------------------------------------------------------------------------
    def OnClick_PageDec(self, event):
        self.callback_page_dec()
