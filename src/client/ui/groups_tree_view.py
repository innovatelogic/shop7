import wx

class GroupsTreeView(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, ms_connection, parent, id, position, size, style):
        '''Initialize our tree
        '''
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
        self.ms_connection = ms_connection
        
        #root = self.AddRoot('Programmer')
        #os = self.AppendItem(root, 'Operating Systems')
        #pl = self.AppendItem(root, 'Programming Languages')
        #tk = self.AppendItem(root, 'Toolkits')
        
        #self.AppendItem(os, 'Linux')
        #self.AppendItem(os, 'FreeBSD')
        #self.AppendItem(os, 'OpenBSD')
        #self.AppendItem(os, 'NetBSD')
        #self.AppendItem(os, 'Solaris')
        
        #
        
        groups = self.ms_connection.send(str({'opcode': 'get_groups', 'id':-2, 'token':0}))
        
        root = self.AddRoot(groups[0]['name'])
        for i in groups[1:]:
            ch = self.AppendItem(root, i['name'])
            self.SetItemHasChildren(ch);
        
        
        
        
        #self.AppendItem(os, 'Linux')
        
        wx.EVT_TREE_ITEM_EXPANDING(self, self.GetId(), self.OnExpanding)
        
    def setEvents(self):
        pass
    
    def OnExpanding(self, event):
        item = event.GetItem()
        self.AppendItem(item, 'Java')
        self.AppendItem(item, 'C++')
        self.AppendItem(item, 'C')
        self.AppendItem(item, 'Pascal')
        
        