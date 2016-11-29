import wx
from groups_tree_view import GroupsTreeView

class EPanelCategory:
    EPanel_Base = 0
    EPanel_Secondary = 1
    EPanel_MAX = 2

#----------------------------------------------------------------------------------------------
class CategoryTreesPanel(wx.Panel):
    def __init__(self, cases_controller, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.realm = cases_controller.realm()
        self.cases_controller = cases_controller
        self.view_panels = []
        self.doLayout()
        self.aspect = ''
        self.TogglePanel(EPanelCategory.EPanel_Base)

#----------------------------------------------------------------------------------------------
    def doLayout(self):
        self.base_tree = GroupsTreeView(self, 1, wx.DefaultPosition, (-1, -1),
                                        wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT)
        
        self.secondary_tree = GroupsTreeView(self, 1, wx.DefaultPosition, (-1, -1),
                                        wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT)
        
        self.view_panels.append(self.base_tree)
        self.view_panels.append(self.secondary_tree)
        
        self.gridsizer = wx.FlexGridSizer(cols=1, rows = 1)
        self.gridsizer.AddGrowableRow(0)
        self.gridsizer.AddGrowableCol(0)
           
        self.SetSizer(self.gridsizer)
        self.bind()
        self.Layout()

#----------------------------------------------------------------------------------------------
    def bind(self):
        self.base_tree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandingTreeNode_User)
        self.base_tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapseTreeNode_User)
        self.base_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChangedTreeNode_User)
        self.secondary_tree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandingTreeNode_Secondary)
        self.secondary_tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapseTreeNode_Secondary)
        self.secondary_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChangedTreeNode_Secondary)
        
#----------------------------------------------------------------------------------------------
    def PopulateBaseList(self):
        categories = self.realm.get_user_categiries_1st_lvl()
        self.base_tree.DeleteAllItems()
        self.base_tree.init_list(categories)

#----------------------------------------------------------------------------------------------
    def PopulateSecondaryList(self, aspect):
        self.aspect = aspect
        categories = self.realm.get_categiries_1st_lvl(aspect)
        self.secondary_tree.DeleteAllItems()
        self.secondary_tree.init_list(categories)
        
#----------------------------------------------------------------------------------------------
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
    
#----------------------------------------------------------------------------------------------
    def OnExpandingTreeNode_User(self, event):
        ''' binds to on node expand event'''
        item = event.GetItem()
        self.cases_controller.expandUserAspectCategory(self.base_tree.GetPyData(item), item)

#----------------------------------------------------------------------------------------------        
    def OnCollapseTreeNode_User(self, event):
        ''' binds to on node collapse event'''
        #item = event.GetItem()
        #self.cases_controller.expandUserAspectCategory(self.base_tree.GetPyData(item), item)
        pass
        
#----------------------------------------------------------------------------------------------
    def OnSelChangedTreeNode_User(self, event):
        item =  event.GetItem()
        self.cases_controller.categoryUserAspectSelected(self.base_tree.GetPyData(item))

#----------------------------------------------------------------------------------------------
    def OnExpandingTreeNode_Secondary(self, event):
        item = event.GetItem()
        self.cases_controller.expandBaseAspectCategory(self.aspect, self.secondary_tree.GetPyData(item), item)

#----------------------------------------------------------------------------------------------        
    def OnCollapseTreeNode_Secondary(self, event):
        ''' binds to on node collapse event'''
        self.secondary_tree.delete_childs(event.GetItem())
        pass
#----------------------------------------------------------------------------------------------
    def OnSelChangedTreeNode_Secondary(self, event):
        item =  event.GetItem()
        self.cases_controller.categoryBaseAspectSelected(self.aspect, self.secondary_tree.GetPyData(item))