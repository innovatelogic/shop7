import wx

class GroupsTreeView(wx.TreeCtrl):
    '''Our customized TreeCtrl class
    '''
    def __init__(self, parent, id, position, size, style):
        '''Initialize our tree
        '''
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
        root = self.AddRoot('Programmer')
        os = self.AppendItem(root, 'Operating Systems')
        pl = self.AppendItem(root, 'Programming Languages')
        tk = self.AppendItem(root, 'Toolkits')
        self.AppendItem(os, 'Linux')
        self.AppendItem(os, 'FreeBSD')
        self.AppendItem(os, 'OpenBSD')
        self.AppendItem(os, 'NetBSD')
        self.AppendItem(os, 'Solaris')
        cl = self.AppendItem(pl, 'Compiled languages')
        sl = self.AppendItem(pl, 'Scripting languages')
        self.AppendItem(cl, 'Java')
        self.AppendItem(cl, 'C++')
        self.AppendItem(cl, 'C')
        self.AppendItem(cl, 'Pascal')
        self.AppendItem(sl, 'Python')
        self.AppendItem(sl, 'Ruby')
        self.AppendItem(sl, 'Tcl')
        self.AppendItem(sl, 'PHP')
        self.AppendItem(tk, 'Qt')
        self.AppendItem(tk, 'MFC')
        self.AppendItem(tk, 'wxPython')
        self.AppendItem(tk, 'GTK+')
        self.AppendItem(tk, 'Swing')