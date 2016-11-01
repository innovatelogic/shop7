import wx
from bson.objectid import ObjectId

class GroupsTreeView(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, realm, parent, id, position, size, style):
        '''Initialize our tree
        '''
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
        self.realm = realm
        
        result = self.realm.ms_connection().send_msg('get_groups', {'id':1})
        
        groups = result['res']
        
        root = self.AddRoot(groups[0]['name'])
        
        for i in groups[1:]:
            ch = self.AppendItem(root, i['name'], -1, -1, wx.TreeItemData(i['_id']))
            
            if i['n_childs'] != '0':
                self.SetItemHasChildren(ch);
        
        wx.EVT_TREE_ITEM_EXPANDING(self, self.GetId(), self.OnExpanding)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        
    def setEvents(self):
        pass
    
    def OnExpanding(self, event):
        item = event.GetItem()
        
        _id = self.GetPyData(item)
        
        result = self.realm.ms_connection().send_msg('get_category_childs', {'id':str(_id)})
        
        groups = result['res']
        
        for i in groups[1:]:
            ch = self.AppendItem(item, i['name'], -1, -1, wx.TreeItemData(i['_id']))
            
            if i['n_childs'] != '0':
                self.SetItemHasChildren(ch);
        pass
    
    def OnSelChanged(self, event):
        item =  event.GetItem()
        _id = self.GetPyData(item)
        
        items = self.realm.ms_connection().send_msg('get_items', {'category_id':str(_id), 'offset':0})
        self.GetParent().GetParent().update_list(items)