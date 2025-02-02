import wx
from items_controller_panel import ItemsControllerPanel
from items_list_panel import ItemsListPanel

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemsMainPanel(wx.Panel):
    def __init__(self, 
                 cases_controller, 
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.cases_controller = cases_controller
        self.realm = cases_controller.realm()
        self.doLayout()

#----------------------------------------------------------------------------------------------
    def doLayout(self):
        self.toppanel = ItemsControllerPanel(self.cases_controller, self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        self.bottompanel = ItemsListPanel(self.cases_controller, self, wx.ID_ANY)
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.toppanel, 0, wx.EXPAND)
        vsizer.Add(self.bottompanel, 1, wx.GROW)
        
        self.SetSizer(vsizer)
        self.Layout()
        
#----------------------------------------------------------------------------------------------
    def process_user_category_selection(self, cat_id):
        print ('[process_user_selection]')
        
#----------------------------------------------------------------------------------------------
    def process_category_selection(self, aspect, cat_id):
        items = self.realm.get_items(aspect, cat_id, 0, 50)
        self.bottompanel.update_list(items)