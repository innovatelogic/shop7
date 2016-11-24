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

#----------------------------------------------------------------------------------------------        
    def OnCheckItem(self, index, flag):
        print(index, flag)

#----------------------------------------------------------------------------------------------                
class DocumentViewPanel(wx.Panel):
    def __init__(self, cases_controller, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.cases_controller.setView(self)
        self.realm = self.cases_controller.realm()
        self.doLayout()

#----------------------------------------------------------------------------------------------        
    def doLayout(self):
        self.split1 = wx.SplitterWindow(self, style = wx.SP_THIN_SASH)
        
        self.lpanel = CategoriesMainPanel(self.cases_controller, self.split1, wx.ID_ANY, size = (-1, -1), pos = (0, 0))
        self.rpanel = ItemsMainPanel(self.cases_controller, self.split1, wx.ID_ANY)
        
        self.split1.SplitVertically(self.lpanel, self.rpanel)
        self.split1.SetSashGravity(0.25)
        self.split1.SetMinimumPaneSize(250)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.split1, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.split1.SetSashPosition(200, True)

#----------------------------------------------------------------------------------------------        
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

#----------------------------------------------------------------------------------------------
    def ClearColumnImage(self, col):
        self.list_ctrl.SetColumnImage(col, -1)

#----------------------------------------------------------------------------------------------    
    def update_list(self, items):
        
        self.il = wx.ImageList(128, 128)
        
        images=["../res/img/check_0.png",
                "../res/img/check_1.png",
                "../res/img/label_128.png"]
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
            
#----------------------------------------------------------------------------------------------
    def addChildCategoriesTreeUserAspect(self, category_id, childs, item):
        #item = self.lpanel.bottompanel.base_tree.GetItemPyData(wx.TreeItemData(category_id))
        self.lpanel.bottompanel.base_tree.append_childs(childs, item)
        pass
    
#----------------------------------------------------------------------------------------------
    def addChildCategoriesTreeBaseAspect(self, category_id, childs, item):
        #item = self.lpanel.bottompanel.secondary_tree.GetItemPyData(wx.TreeItemData(category_id))
        self.lpanel.bottompanel.secondary_tree.append_childs(childs, item)
        pass
    
#----------------------------------------------------------------------------------------------    
    def fillItemsList(self, items):
        self.rpanel.bottompanel.update_list(items)
        pass