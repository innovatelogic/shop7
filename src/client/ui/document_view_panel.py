import wx
from bson.objectid import ObjectId
from groups_tree_view import GroupsTreeView
from wx.lib.agw import ultimatelistctrl as ULC
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
        
        self.list_ctrl = ULC.UltimateListCtrl(self.bottompanel.right, size=(-1, 800), agwStyle=ULC.ULC_REPORT|ULC.ULC_HAS_VARIABLE_ROW_HEIGHT) #style=wx.LC_REPORT|wx.BORDER_SUNKEN
            
        self.list_ctrl.InsertColumn(0, 'Img')
        self.list_ctrl.InsertColumn(1, 'Name')
        self.list_ctrl.InsertColumn(2, 'Availability')
        self.list_ctrl.InsertColumn(3, 'Amount')
        self.list_ctrl.InsertColumn(4, 'Unit')
        self.list_ctrl.InsertColumn(5, 'Price')
        self.list_ctrl.InsertColumn(6, 'Currency')
        self.list_ctrl.InsertColumn(7, 'Desc')
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        self.bottompanel.right.SetSizer(sizer)
        

    
    def update_list(self, items):
        self.list_ctrl.DeleteAllItems()
        
        il = wx.ImageList(48, 48)
        self.list_ctrl.SetImageList(il, wx.IMAGE_LIST_SMALL)
        images=["../res/tumbnail.jpg"]
        for i in images:
            img = wx.Image(i, wx.BITMAP_TYPE_ANY)
            img = wx.BitmapFromImage(img)
            il.Add(img)
        
        arr = items['res']
        for i in range(len(arr)):
            pos = self.list_ctrl.InsertImageStringItem(i,'', 0)
            self.list_ctrl.SetStringItem(pos, 1, arr[i]['name'])
            self.list_ctrl.SetStringItem(pos, 2, arr[i]['availability'])
            self.list_ctrl.SetStringItem(pos, 3, str(arr[i]['amount']))
            self.list_ctrl.SetStringItem(pos, 4, arr[i]['unit'])
            self.list_ctrl.SetStringItem(pos, 5, str(arr[i]['price']))
            self.list_ctrl.SetStringItem(pos, 6, arr[i]['currency'])
            self.list_ctrl.SetStringItem(pos, 7, arr[i]['desc'])
            
            
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