import wx
from groups_tree_view import GroupsTreeView

class EPanelCategory:
    EPanel_Base = 0
    EPanel_Secondary = 1
    EPanel_MAX = 2

class CategoryTreesPanel(wx.Panel):
    def __init__(self, realm, callback_cat_selected, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = realm 
        self.callback_cat_selected = callback_cat_selected
        self.SetBackgroundColour((255, 0, 0))
        self.view_panels = []
        self.doLayout()
        self.TogglePanel(EPanelCategory.EPanel_Base)
        
    def doLayout(self):
        self.base_panel = wx.Panel(self, wx.ID_ANY, size = (-1, -1))
        self.secondary_tree = self.sec_tree = GroupsTreeView(self.realm, 
                                        self, 1, wx.DefaultPosition, (-1, -1),
                                        wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT)
        
        self.base_panel.SetBackgroundColour((54, 45, 54))
        
        self.view_panels.append(self.base_panel)
        self.view_panels.append(self.secondary_tree)
        
        self.gridsizer = wx.FlexGridSizer(cols=1, rows = 1)
        self.gridsizer.AddGrowableRow(0)
        self.gridsizer.AddGrowableCol(0)
           
        self.SetSizer(self.gridsizer)
        
        self.init_lists()
        
        self.bind()
        
        self.Layout()
        
    def bind(self):
        self.secondary_tree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandingTreeNode)
        self.secondary_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChangedTreeNode) 
        
    def init_lists(self):
        categories = self.realm.get_categiries_1st_lvl('prom')
        self.secondary_tree.init_list(categories)
        
    def TogglePanel(self, index):
        out = None
        self.gridsizer.Clear()
        for i in range(0, EPanelCategory.EPanel_MAX):
            if i == index:
                self.gridsizer.Add(self.view_panels[i], 0, wx.EXPAND)
                self.view_panels[i].Show()
                self.view_panels[i].Layout()
                out = self.view_panels[i]
            else:
                self.view_panels[i].Hide()
        self.Layout()
        return out
    
    def OnExpandingTreeNode(self, event):
        item = event.GetItem()
        categories = self.realm.get_category_childs('prom', self.secondary_tree.GetPyData(item))
        self.secondary_tree.append_childs(categories, item)
    
    def OnSelChangedTreeNode(self, event):
        item =  event.GetItem()
        _id = self.secondary_tree.GetPyData(item)
        
        self.callback_cat_selected('prom', _id)
        #items = self.realm.get_items('prom', _id, 0, 50)
        
        #items = self.realm.ms_connection().send_msg('get_items', {'category_id':str(_id), 'offset':0})
        #self.GetParent().GetParent().update_list(items)