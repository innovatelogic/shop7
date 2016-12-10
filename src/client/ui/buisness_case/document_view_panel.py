import wx
#from bson.objectid import ObjectId
#from ui.proportional_splitter import ProportionalSplitter
from add_item.add_item_main_panel import AddItemMainPanel
from items_view.items_view_panel import ItemsViewPanel

class EPanelsCases:
    EPanel_Items = 0
    EPanel_AddItem = 1
    EPanel_MAX = 2
    
#----------------------------------------------------------------------------------------------                
class DocumentViewPanel(wx.Panel):
    def __init__(self, cases_controller, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.cases_controller.setView(self)
        self.realm = self.cases_controller.realm()
        self.view_panels = []
        self.doLayout()

#----------------------------------------------------------------------------------------------        
    def doLayout(self):
        
        self.gridsizer = wx.FlexGridSizer(cols=1, rows = 1)
        self.gridsizer.AddGrowableRow(0)
        self.gridsizer.AddGrowableCol(0)
        self.SetSizer(self.gridsizer)
        
        self.itemsViewPanel = ItemsViewPanel(self.cases_controller, self, wx.ID_ANY, size = (-1, -1))
        self.addItemPanel = AddItemMainPanel(self.cases_controller, self, wx.ID_ANY, size = (-1, -1))
        
        self.view_panels.append(self.itemsViewPanel)
        self.view_panels.append(self.addItemPanel)
        
        self.itemsViewPanel.SetBackgroundColour(wx.Colour(34, 1, 96))
        self.addItemPanel.SetBackgroundColour(wx.Colour(34, 165, 96))
        
        #self.split1 = wx.SplitterWindow(self, style = wx.SP_THIN_SASH)
        
        #self.lpanel = CategoriesMainPanel(self.cases_controller, self.split1, wx.ID_ANY, size = (-1, -1), pos = (0, 0))
        #self.rpanel = ItemsMainPanel(self.cases_controller, self.split1, wx.ID_ANY)
        
        #self.split1.SplitVertically(self.lpanel, self.rpanel)
        #self.split1.SetSashGravity(0.25)
        #self.split1.SetMinimumPaneSize(250)
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(self.split1, 1, wx.EXPAND)
        #self.SetSizer(sizer)
        #self.split1.SetSashPosition(200, True)
        
        self.TogglePanel(EPanelsCases.EPanel_Items)
        
#----------------------------------------------------------------------------------------------
    def TogglePanel(self, index):
        out = None
        self.gridsizer.Clear()
        for i in range(0, EPanelsCases.EPanel_MAX):
            if i == index:
                self.gridsizer.Add(self.view_panels[i], 0, wx.EXPAND)
                self.view_panels[i].Show()
                self.view_panels[i].Layout()
                out = self.view_panels[i]
            else:
                self.view_panels[i].Hide()
        self.Layout()
        return out

#----------------------------------------------------------------------------------------------
    def addChildCategoriesTreeUserAspect(self, category_id, childs, item):
        #item = self.lpanel.bottompanel.base_tree.GetItemPyData(wx.TreeItemData(category_id))
        self.itemsViewPanel.lpanel.bottompanel.base_tree.append_childs(childs, item)
        pass
    
#----------------------------------------------------------------------------------------------
    def addChildCategoriesTreeBaseAspect(self, category_id, childs, item):
        #item = self.lpanel.bottompanel.secondary_tree.GetItemPyData(wx.TreeItemData(category_id))
        self.itemsViewPanel.lpanel.bottompanel.secondary_tree.append_childs(childs, item)
        pass
    
#----------------------------------------------------------------------------------------------    
    def fillItemsList(self, items):
        self.itemsViewPanel.rpanel.bottompanel.update_list(items)
        pass
    
#----------------------------------------------------------------------------------------------    
    def initPageController(self, state):
        self.itemsViewPanel.rpanel.bottompanel.bottompanel.initController(state)
        pass
    
#----------------------------------------------------------------------------------------------  
    def updatePageController(self, state):
        self.itemsViewPanel.rpanel.bottompanel.bottompanel.updateController(state)
        pass