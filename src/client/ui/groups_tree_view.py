import wx

class GroupsTreeView(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, ms_connection, parent, id, position, size, style):
        '''Initialize our tree
        '''
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
        self.ms_connection = ms_connection
        
        result = self.ms_connection.send(str({'opcode': 'get_groups', 'id':1, 'token':0}))
        
        groups = result['res']
        
        root = self.AddRoot(groups[0]['name'])
        
        for i in groups[1:]:
            ch = self.AppendItem(root, i['name'], -1, -1, wx.TreeItemData(i['_id']))
            
            if i['n_childs'] != '0':
                self.SetItemHasChildren(ch);
        
        wx.EVT_TREE_ITEM_EXPANDING(self, self.GetId(), self.OnExpanding)
        
    def setEvents(self):
        pass
    
    def OnExpanding(self, event):
        item = event.GetItem()
        
        _id = self.GetPyData(item)
        
        result = self.ms_connection.send(str({'opcode': 'get_category_childs', 'id':str(_id), 'token':0}))
        
        print result
        
        groups = result['res']
        
        for i in groups[1:]:
            ch = self.AppendItem(item, i['name'], -1, -1, wx.TreeItemData(i['_id']))
            
            if i['n_childs'] != '0':
                self.SetItemHasChildren(ch);
        pass
        
        