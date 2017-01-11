import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from items_list_bottom_control_panel import ItemsListBottomControlPanel

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(-1, -1), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        
    def OnCheckItem(self, index, flag):
        print(index, flag)

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemsListPanel(wx.Panel):
    def __init__(self, 
                 cases_controller,
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = cases_controller.realm()
        self.cases_controller = cases_controller
        self.list_column_map = {}
        self.doLayout()

#----------------------------------------------------------------------------------------------
    def doLayout(self):
        self.toppanel = wx.Panel(self, wx.ID_ANY, size=(-1, 25))
        self.bottompanel = ItemsListBottomControlPanel(self.cases_controller,
                                                       self, wx.ID_ANY, size=(-1, 30))
        gridsizer = wx.FlexGridSizer(cols=1, rows = 2)
        gridsizer.AddGrowableRow(0)
        gridsizer.AddGrowableCol(0)
        
        gridsizer.Add(self.toppanel, flag = wx.ALL|wx.EXPAND)
        gridsizer.Add(self.bottompanel, flag = wx.ALL|wx.EXPAND)
        self.SetSizer(gridsizer)
        
        self.split = wx.SplitterWindow(self.toppanel, style = wx.SP_THIN_SASH)
        
        self.list_ctrl = CheckListCtrl(self.split)
        self.rpanel = wx.Panel(self.split, wx.ID_ANY, size=(-1, 125))
        
        self.split.SplitVertically(self.list_ctrl, self.rpanel)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.split, 1, wx.EXPAND)
        self.toppanel.SetSizer(sizer)
        self.split.SetSashPosition(200, True)
        
        list_gridsizer = wx.FlexGridSizer(cols=1, rows = 2)
        list_gridsizer.AddGrowableRow(0)
        list_gridsizer.AddGrowableCol(0)
        list_gridsizer.Add(self.list_ctrl, flag = wx.ALL|wx.EXPAND)
        self.split.SetSizer(list_gridsizer)
        
        user_settings = self.realm.getUserSettings()
        self.toggleItemPreveiewColumn(user_settings.options['client']['ui']['cases']['item_preview_column'])
        
        self.initListCtrl()
        self.Layout()
        
#----------------------------------------------------------------------------------------------
    def toggleItemPreveiewColumn(self, flag):
        if not flag:
            self.split.Unsplit(self.rpanel)
        else:
            self.split.SplitVertically(self.list_ctrl, self.rpanel)
        
#----------------------------------------------------------------------------------------------
    def initListCtrl(self):
        self.list_column_map = {}
        self.list_ctrl.ClearAll()
        
        info = self.cases_controller.getItemsListInfo()

        n_count = 0
        for i in info:
            if i[1]:
              self.list_ctrl.InsertColumn(n_count, i[0])
              self.list_column_map[i[0].lower()] = n_count
              n_count += 1
        
        if n_count > 0:
            self.list_ctrl.SetColumnWidth(0, 25)
            if n_count >= 1:    
                self.list_ctrl.SetColumnWidth(1, 128)
            self.list_ctrl.setResizeColumn(n_count)

#----------------------------------------------------------------------------------------------
    def update_list(self, items):
        
        self.il = wx.ImageList(128, 128)
        
        images=["../res/img/check_0.png", "../res/img/check_1.png", "../res/img/label_128.png"]
        for i in images:
            img = wx.Image(i, wx.BITMAP_TYPE_ANY)
            img = wx.BitmapFromImage(img)
            self.il.Add(img)
            
        self.list_ctrl.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.list_ctrl.DeleteAllItems()
        
        for i in items['res']:
            pos = self.list_ctrl.Append([''])
            
            if 'name' in self.list_column_map:
                self.list_ctrl.SetStringItem(pos, self.list_column_map['name'], i['name'])
            if 'availability' in self.list_column_map:   
                self.list_ctrl.SetStringItem(pos, self.list_column_map['availability'], i['availability'])
            if 'amount' in self.list_column_map:
                self.list_ctrl.SetStringItem(pos, self.list_column_map['amount'], str(i['amount']))
            if 'unit' in self.list_column_map:
                self.list_ctrl.SetStringItem(pos, self.list_column_map['unit'], i['unit'])
            if 'price' in self.list_column_map:
                self.list_ctrl.SetStringItem(pos, self.list_column_map['price'], str(i['price']))
            if 'currency' in self.list_column_map:    
                self.list_ctrl.SetStringItem(pos, self.list_column_map['currency'], i['currency'])
            if 'desc' in self.list_column_map:    
                self.list_ctrl.SetStringItem(pos, self.list_column_map['desc'], i['desc'])
            
            #item = self.list_ctrl.GetItem(pos)
            if 'img' in self.list_column_map:
                self.list_ctrl.SetItemColumnImage(pos, self.list_column_map['img'], 2)