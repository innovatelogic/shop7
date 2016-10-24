import wx
from bson.objectid import ObjectId
from groups_tree_view import GroupsTreeView
from wx.lib.agw import ultimatelistctrl as ULC
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
#from ObjectListView import ObjectListView, ColumnDefn

class Book(object):
    """
    Model of the Book object
 
    Contains the following attributes:
    'ISBN', 'Author', 'Manufacturer', 'Title'
    """
    #----------------------------------------------------------------------
    def __init__(self, title, author, isbn, mfg):
        self.isbn = isbn
        self.author = author
        self.mfg = mfg
        self.title = title
        
class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(-1, 800), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
                
class DocumentViewPanel(wx.Panel):
    def __init__(self, connection_info, ms_connection, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.connection_info = connection_info
        self.ms_connection = ms_connection
        self.SetBackgroundColour((255, 255, 255))
        self.doLayout()
        
    def doLayout(self):
        W,H = self.GetSize()
        self.toppanel = wx.Panel(self, wx.ID_ANY, size = (-1, 45), pos = (0, 0))
        self.toppanel.SetBackgroundColour((215, 215, 215))
        self.bottompanel = wx.Panel(self, wx.ID_ANY)
        self.bottompanel.SetBackgroundColour((255, 255, 255))
        
        posCenterPanelVertSzr = wx.BoxSizer(wx.VERTICAL)
        posCenterPanelVertSzr.Add(self.toppanel, 0, wx.EXPAND)
        posCenterPanelVertSzr.Add(self.bottompanel, 1, wx.GROW)
        self.SetSizer(posCenterPanelVertSzr)
                
        self.bottompanel.left_tree = GroupsTreeView(self.ms_connection, self.bottompanel, 1, wx.DefaultPosition, (250, -1),
                                                                 wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT)
        self.bottompanel.right = wx.Panel(self.bottompanel, wx.ID_ANY)
        self.bottompanel.right.SetBackgroundColour((235, 235, 235))
        
        posDocHorSzr = wx.BoxSizer(wx.HORIZONTAL)
        posDocHorSzr.Add(self.bottompanel.left_tree, 0, wx.EXPAND)
        posDocHorSzr.Add(self.bottompanel.right, 1, wx.GROW)
        self.bottompanel.SetSizer(posDocHorSzr)

        self.list_ctrl = CheckListCtrl(self.bottompanel.right) #style=wx.LC_REPORT|wx.BORDER_SUNKEN
        #, size=(-1, 800), style=wx.LC_REPORT| wx.BORDER_NONE
        #                         | wx.LC_EDIT_LABELS
        #                         | wx.LC_SORT_ASCENDING
        info = wx.ListItem()
        info._mask = wx.LIST_MASK_TEXT| wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        info.m_text = "Img"
        
        self.list_ctrl.InsertColumnInfo(0, info)
        
        info.m_image = 0
        self.list_ctrl.InsertColumnInfo(1, info)
        
        self.list_ctrl.InsertColumn(2, 'Name')
        self.list_ctrl.InsertColumn(3, 'Availability')
        self.list_ctrl.InsertColumn(4, 'Amount')
        self.list_ctrl.InsertColumn(5, 'Unit')
        self.list_ctrl.InsertColumn(6, 'Price')
        self.list_ctrl.InsertColumn(7, 'Currency')
        self.list_ctrl.InsertColumn(8, 'Desc')
        
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
        
        self.il = wx.ImageList(48, 48)
        
        images=["../res/tumbnail.jpg"]
        for i in images:
            img = wx.Image(i, wx.BITMAP_TYPE_ANY)
            img = wx.BitmapFromImage(img)
            self.il.Add(img)
            
        self.list_ctrl.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        
        self.list_ctrl.DeleteAllItems()
        
        arr = items['res']
        for i in range(len(arr)):
            pos = self.list_ctrl.InsertImageStringItem(i,'', 0)
            self.list_ctrl.SetStringItem(pos, 2, arr[i]['name'])
            self.list_ctrl.SetStringItem(pos, 3, arr[i]['availability'])
            self.list_ctrl.SetStringItem(pos, 4, str(arr[i]['amount']))
            self.list_ctrl.SetStringItem(pos, 5, arr[i]['unit'])
            self.list_ctrl.SetStringItem(pos, 6, str(arr[i]['price']))
            self.list_ctrl.SetStringItem(pos, 7, arr[i]['currency'])
            self.list_ctrl.SetStringItem(pos, 8, arr[i]['desc'])
            
            item = self.list_ctrl.GetItem(pos)
            self.list_ctrl.SetItemColumnImage(pos, 1, 0)
            
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