import wx

TITLE_DLG = "Buisness___"

class DocumentFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=TITLE_DLG, size=(800, 600))
        
        self.statusbar = self.CreateStatusBar()
        
        self.Show(True)