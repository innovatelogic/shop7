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
    def __init__(self, realm, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = realm
        self.doLayout()

#----------------------------------------------------------------------------------------------
    def doLayout(self):
        self.toppanel = wx.Panel(self, wx.ID_ANY, size=(-1, 25))
        self.bottompanel = ItemsListBottomControlPanel(self, wx.ID_ANY, size=(-1, 30))
      
        self.list_ctrl = self.initListCtrl(self.toppanel)
        
        gridsizer = wx.FlexGridSizer(cols=1, rows = 2)
        gridsizer.AddGrowableRow(0)
        gridsizer.AddGrowableCol(0)
        
        gridsizer.Add(self.toppanel, flag = wx.ALL|wx.EXPAND)
        gridsizer.Add(self.bottompanel, flag = wx.ALL|wx.EXPAND)
        
        list_gridsizer = wx.FlexGridSizer(cols=1, rows = 2)
        list_gridsizer.AddGrowableRow(0)
        list_gridsizer.AddGrowableCol(0)
        list_gridsizer.Add(self.list_ctrl, flag = wx.ALL|wx.EXPAND)
        self.toppanel.SetSizer(list_gridsizer)
        
        self.SetSizer(gridsizer)
        
        self.Layout()

#----------------------------------------------------------------------------------------------
    def initListCtrl(self, parent):
        list_ctrl = CheckListCtrl(parent)
        
        list_ctrl.InsertColumn(0, '')
        list_ctrl.InsertColumn(1, 'Img')
        list_ctrl.InsertColumn(2, 'Name')
        list_ctrl.InsertColumn(3, 'Availability')
        list_ctrl.InsertColumn(4, 'Amount')
        list_ctrl.InsertColumn(5, 'Unit')
        list_ctrl.InsertColumn(6, 'Price')
        list_ctrl.InsertColumn(7, 'Currency')
        list_ctrl.InsertColumn(8, 'Desc')
        
        list_ctrl.SetColumnWidth(0, 25)
        list_ctrl.SetColumnWidth(1, 128)
        list_ctrl.setResizeColumn(9)
        return list_ctrl

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
        
        arr = items['res']
        for i in range(len(arr)):
            pos = self.list_ctrl.Append([''])
            self.list_ctrl.SetStringItem(pos, 2, arr[i]['name'])
            self.list_ctrl.SetStringItem(pos, 3, arr[i]['availability'])
            self.list_ctrl.SetStringItem(pos, 4, str(arr[i]['amount']))
            self.list_ctrl.SetStringItem(pos, 5, arr[i]['unit'])
            self.list_ctrl.SetStringItem(pos, 6, str(arr[i]['price']))
            self.list_ctrl.SetStringItem(pos, 7, arr[i]['currency'])
            self.list_ctrl.SetStringItem(pos, 8, arr[i]['desc'])
            
            #item = self.list_ctrl.GetItem(pos)
            #self.list_ctrl.SetItemColumnImage(pos, 0, 1)
            
            item = self.list_ctrl.GetItem(pos)
            self.list_ctrl.SetItemColumnImage(pos, 1, 2)