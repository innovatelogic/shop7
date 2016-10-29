import wx
from bson.objectid import ObjectId
from categories_main_panel import CategoriesMainPanel
from items_main_panel import ItemsMainPanel
from ui.proportional_splitter import ProportionalSplitter
from groups_tree_view import GroupsTreeView

from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
        
class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(-1, 800), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        
    def OnCheckItem(self, index, flag):
        print(index, flag)
                
class DocumentViewPanel(wx.Panel):
    def __init__(self, connection_info, ms_connection, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.connection_info = connection_info
        self.ms_connection = ms_connection
        self.SetBackgroundColour((255, 255, 255))
        self.doLayout()
        
    def doLayout(self):
        self.split1 = wx.SplitterWindow(self, style = wx.SP_THIN_SASH)
        
        W,H = self.GetSize()
        self.lpanel = CategoriesMainPanel(self.connection_info, self.ms_connection, self.split1, wx.ID_ANY, size = (-1, -1), pos = (0, 0))
        self.rpanel = ItemsMainPanel(self.connection_info, self.ms_connection, self.split1, wx.ID_ANY)
        
        self.split1.SplitVertically(self.lpanel, self.rpanel)
        self.split1.SetSashGravity(0.25)
        self.split1.SetMinimumPaneSize(250)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.split1, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.split1.SetSashPosition(200, True)

        #posCenterPanelVertSzr = wx.BoxSizer(wx.HORIZONTAL)
        #posCenterPanelVertSzr.Add(self.lpanel, 0, wx.EXPAND)
        #posCenterPanelVertSzr.Add(self.rpanel, 1, wx.GROW)
        
        #self.SetSizer(posCenterPanelVertSzr)
        return
    
        self.bottompanel.left_tree = GroupsTreeView(self.ms_connection, 
                                                    self.bottompanel, 1, wx.DefaultPosition, (250, -1),
                                                    wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT)
        
        self.bottompanel.right = wx.Panel(self.bottompanel, wx.ID_ANY)
        self.bottompanel.right.SetBackgroundColour((235, 235, 235))
        
        posDocHorSzr = wx.BoxSizer(wx.HORIZONTAL)
        posDocHorSzr.Add(self.bottompanel.left_tree, 0, wx.EXPAND)
        posDocHorSzr.Add(self.bottompanel.right, 1, wx.GROW)
        self.bottompanel.SetSizer(posDocHorSzr)

        self.list_ctrl = CheckListCtrl(self.bottompanel.right)
        
        #self.list_ctrl.InsertColumnInfo(0, info)
        
        #self.list_ctrl.InsertColumnInfo(1, info)
        self.list_ctrl.InsertColumn(0, '')
        self.list_ctrl.InsertColumn(1, 'Img')
        self.list_ctrl.InsertColumn(2, 'Name')
        self.list_ctrl.InsertColumn(3, 'Availability')
        self.list_ctrl.InsertColumn(4, 'Amount')
        self.list_ctrl.InsertColumn(5, 'Unit')
        self.list_ctrl.InsertColumn(6, 'Price')
        self.list_ctrl.InsertColumn(7, 'Currency')
        self.list_ctrl.InsertColumn(8, 'Desc')
        
        self.list_ctrl.SetColumnWidth(0, 25)
        self.list_ctrl.SetColumnWidth(1, 128)
        self.list_ctrl.setResizeColumn(9)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        self.bottompanel.right.SetSizer(sizer)
        
    def SetColumnImage(self, col, image):
         item = self.list_ctrl.GetColumn(col)
         # preserve all other attributes too
         item.SetMask( wx.LIST_MASK_STATE |
                       wx.LIST_MASK_TEXT  |
                       wx.LIST_MASK_IMAGE |
                       wx.LIST_MASK_DATA  |
                       wx.LIST_SET_ITEM   |
                       wx.LIST_MASK_WIDTH |
                       wx.LIST_MASK_FORMAT )
         item.SetImage(image)
         self.list_ctrl.SetColumn(col, item)

    def ClearColumnImage(self, col):
        self.list_ctrl.SetColumnImage(col, -1)
    
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
            
            #SetColumnImage(0,0)
            #self.SetColumnImage(1,0)
        ################################
        #self.products = [Book("wxPython in Action", "Robin Dunn",
        #                      "1932394621", "Manning"),
        #                 Book("Hello World", "Warren and Carter Sande",
        #                      "1933988495", "Manning")
        #                 ]
 
        #self.dataOlv = ObjectListView(self.bottompanel.right, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        #self.setBooks()
        
        # Allow the cell values to be edited when double-clicked
        #self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK
        
    #####################################    
    #def setBooks(self, data=None):
    #    self.dataOlv.SetColumns([
   #        ColumnDefn("Title", "left", 220, "title"),
    #        ColumnDefn("Author", "left", 200, "author"),
    #        ColumnDefn("ISBN", "right", 100, "isbn"),            
    #        ColumnDefn("Mfg", "left", 180, "mfg")
    #    ])
    #    self.dataOlv.SetObjects(self.products)