import wx

class GroupsTreeView(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, ms_connection, parent, id, position, size, style):
        '''Initialize our tree
        '''
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
        self.ms_connection = ms_connection
        
        groups = self.ms_connection.send(str({'opcode': 'get_groups', 'id':1, 'token':0}))
        
        root = self.AddRoot(groups[0]['name'])
        for i in groups[1:]:
            ch = self.AppendItem(root, i['name'])
            self.SetPyData(ch, wx.TreeItemData(i['_id']))
            self.SetItemHasChildren(ch);
        
        wx.EVT_TREE_ITEM_EXPANDING(self, self.GetId(), self.OnExpanding)
        
    def setEvents(self):
        pass
    
    def OnExpanding(self, event):
        item = event.GetItem()
        #self.AppendItem(item, 'Java')
        #self.AppendItem(item, 'C++')
        #self.AppendItem(item, 'C')
        #self.AppendItem(item, 'Pascal')
        pass
        
        