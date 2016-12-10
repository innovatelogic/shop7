import wx
from items_view.categories_main_panel import CategoriesMainPanel
from items_view.items_main_panel import ItemsMainPanel

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemsViewPanel(wx.Panel):
    def __init__(self, cases_controller, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.realm = self.cases_controller.realm()
        self.doLayout()
        pass
    
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