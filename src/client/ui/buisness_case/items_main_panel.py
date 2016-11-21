import wx
from items_controller_panel import ItemsControllerPanel
from items_list_panel import ItemsListPanel

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemsMainPanel(wx.Panel):
    def __init__(self, realm, 
                 callback_add_item,
                 callback_edit_item,
                 callback_del_item,
                 callback_column_change,
                 parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.callback_add_item = callback_add_item
        self.callback_edit_item = callback_edit_item
        self.callback_del_item = callback_del_item
        self.callback_column_change = callback_column_change
        self.realm = realm
        self.doLayout()

#----------------------------------------------------------------------------------------------
    def doLayout(self):
        self.toppanel = ItemsControllerPanel(self.realm,
                                             self.callback_column_change,
                                             self, wx.ID_ANY, size = (-1, 40), pos = (0, 0))
        self.bottompanel = ItemsListPanel(self.realm, self, wx.ID_ANY)
        
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