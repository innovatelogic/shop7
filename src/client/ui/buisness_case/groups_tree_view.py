import wx

class GroupsTreeView(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, parent, id, position, size, style):
        '''Initialize our tree
        '''
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)

#----------------------------------------------------------------------------------------------
    def init_list(self, items):
        root = self.AddRoot(items[0]['name'])
        for item in items[1:]:
            ch = self.AppendItem(root, item['name'], -1, -1, wx.TreeItemData(item['_id']))
            
            if item['n_childs'] != '0':
                self.SetItemHasChildren(ch);

#----------------------------------------------------------------------------------------------
    def append_childs(self, items, parent_item):
        items_data = []
        item, cookie = self.GetFirstChild(parent_item)
        while item.IsOk():
            items_data.append(self.GetPyData(item))
            item, cookie = self.GetNextChild(parent_item, cookie)
            
        for item in items[1:]:
            if item['_id'] not in items_data:
                ch = self.AppendItem(parent_item, item['name'], -1, -1, wx.TreeItemData(item['_id']))
            
                if item['n_childs'] != '0':
                    self.SetItemHasChildren(ch);
                    
#----------------------------------------------------------------------------------------------                    
    def delete_childs(self, parent_item):
        item, cookie = self.GetFirstChild(parent_item)
        while item.IsOk():
            self.DeleteChildren(item)
            item, cookie = self.GetNextChild(parent_item, cookie)