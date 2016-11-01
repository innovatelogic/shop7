import wx

class GroupsTreeView(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, realm, parent, id, position, size, style):
        '''Initialize our tree
        '''
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
        self.realm = realm
    
    def init_list(self, items):
        root = self.AddRoot(items[0]['name'])
        for item in items[1:]:
            ch = self.AppendItem(root, item['name'], -1, -1, wx.TreeItemData(item['_id']))
            
            if item['n_childs'] != '0':
                self.SetItemHasChildren(ch);

    def append_childs(self, items, parent_item):
        for item in items[1:]:
            ch = self.AppendItem(parent_item, item['name'], -1, -1, wx.TreeItemData(item['_id']))
            
            if item['n_childs'] != '0':
                self.SetItemHasChildren(ch);