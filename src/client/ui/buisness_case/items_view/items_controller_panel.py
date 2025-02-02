import wx
import wx.lib.agw.gradientbutton as GB

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ButtonPanel(wx.Panel):
    COLOR_DARK_BLUE_THEME = wx.Colour(34, 65, 96)
    BTN_WIDTH = 40
    BTN_HEIGHT = 30
    SHIFT = 5
    
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.buttons = []
        self.doLayout()
        
    def doLayout(self):
        self.add_button = GB.GradientButton(self, label="Add", pos = (0, 0), size = (self.BTN_WIDTH, self.BTN_HEIGHT))
        self.edit_button = GB.GradientButton(self, label="Edit", pos = (self.BTN_WIDTH + self.SHIFT, 0), size = (self.BTN_WIDTH, self.BTN_HEIGHT))
        self.del_button = GB.GradientButton(self, label="Del", pos = ((self.BTN_WIDTH + self.SHIFT) * 2, 0), size = (self.BTN_WIDTH, self.BTN_HEIGHT))
    
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemsControllerPanel(wx.Panel):
    COLOR_LIGHT_GRAY_THEME = wx.Colour(215, 215, 215)
    IMAGE_DROPDOWN = "../res/img/dropdown.png"
    COLUMN_LABEL="columns"
    LABEL_SHOW_ITEM_PREVIEW="item preview"
    
    def __init__(self, 
                 cases_controller, 
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.realm = cases_controller.realm()
        self.doLayout()
        self.initPopupMenu()
        self.bind()
 
#----------------------------------------------------------------------------------------------
    def doLayout(self):
        gridsizer = wx.FlexGridSizer(cols=5, rows = 1)
        gridsizer.AddGrowableRow(0)
        gridsizer.AddGrowableCol(1)
        gridsizer.AddGrowableCol(3)
        
        sizer_0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btnpanel = ButtonPanel(self, wx.ID_ANY, pos = (0, 0), size = (140, -1))
        self.inputTxt = wx.TextCtrl(self, wx.ID_ANY, '', size=(250, 25))
        bmp_search = wx.Bitmap(self.IMAGE_DROPDOWN, wx.BITMAP_TYPE_ANY)
        self.search_btn = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_search, size = (20, 20))
        self.columns_btn = wx.BitmapButton(self, wx.NewId(), bitmap=bmp_search, size = (20, 20))
        self.columns_name = wx.StaticText(self, label=self.COLUMN_LABEL, pos=(10, 10))
        
        sizer_0.Add((40,-1), 1, wx.EXPAND) # this is a spacer
        sizer_0.Add(self.btnpanel, flag = wx.ALIGN_CENTER_VERTICAL)
        
        sizer_1.Add((20,-1), 1, wx.EXPAND) # this is a spacer
        
        sizer_2.Add(self.inputTxt, flag = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer_2.Add((5,-1), 1, wx.EXPAND) 
        sizer_2.Add(self.search_btn, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        
        sizer_3.Add((20,-1), 1, wx.EXPAND) # this is a spacer
        
        sizer_4.Add(self.columns_name, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer_4.Add((5,-1), 1, wx.EXPAND) # this is a spacer
        sizer_4.Add(self.columns_btn, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer_4.Add((15,-1), 1, wx.EXPAND) # this is a spacer
        
        gridsizer.Add(sizer_0, flag = wx.EXPAND) 
        gridsizer.Add(sizer_1, flag = wx.EXPAND) 
        gridsizer.Add(sizer_2, flag = wx.EXPAND)
        gridsizer.Add(sizer_3, flag = wx.EXPAND)
        gridsizer.Add(sizer_4, flag = wx.EXPAND)
        
        self.SetSizer(gridsizer)

#----------------------------------------------------------------------------------------------
    def bind(self):
        self.Bind(wx.EVT_BUTTON, self.OnClick_ColumnsCheck, self.columns_btn)
        self.Bind(wx.EVT_BUTTON, self.OnClick_AddItem, self.btnpanel.add_button)
        self.Bind(wx.EVT_BUTTON, self.OnClick_EditItem, self.btnpanel.edit_button)
        self.Bind(wx.EVT_BUTTON, self.OnClick_DelItem, self.btnpanel.del_button)
        pass
    
#----------------------------------------------------------------------------------------------
    def initPopupMenu(self):
        user_settings = self.realm.getUserSettings()
        
        self.popupmenu = wx.Menu()
        radios = []
        for key, value in user_settings.options['client']['ui']['cases']['item_columns'].iteritems():
            item = self.popupmenu.AppendCheckItem(-1, key)
            self.popupmenu.Check(item.GetId(), value)
            self.Bind(wx.EVT_MENU, self.OnPopupItemColumnSelected, item)
        
        self.popupmenu.AppendSeparator()
        item_show_preview = self.popupmenu.AppendCheckItem(-1, self.LABEL_SHOW_ITEM_PREVIEW)
        self.Bind(wx.EVT_MENU, self.onPopupItemShowItemPreview, item_show_preview)
        
        show_preview = user_settings.options['client']['ui']['cases']['item_preview_column']
        self.popupmenu.Check(item_show_preview.GetId(), show_preview)

#----------------------------------------------------------------------------------------------
    def OnShowPopup(self, pos):
        cl_pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, cl_pos)
        
#----------------------------------------------------------------------------------------------
    def OnPopupItemSelected(self, event):
        pass

#----------------------------------------------------------------------------------------------
    def OnPopupItemColumnSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        self.cases_controller.itemColumnSettingsChange(item.GetText(), item.IsChecked())

#----------------------------------------------------------------------------------------------
    def onPopupItemShowItemPreview(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        self.cases_controller.toggleItemPreviewColumn(item.IsChecked())
        
#----------------------------------------------------------------------------------------------
    def OnClick_ColumnsCheck(self, event):
        pos = self.columns_btn.GetScreenPosition()
        pos[0] += 20
        cl_pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, cl_pos)

#----------------------------------------------------------------------------------------------
    def OnClick_AddItem(self, event):
        self.cases_controller.addItem()

#----------------------------------------------------------------------------------------------
    def OnClick_EditItem(self, event):
        self.cases_controller.editItem()
        
#----------------------------------------------------------------------------------------------
    def OnClick_DelItem(self, event):
        self.cases_controller.delItem()