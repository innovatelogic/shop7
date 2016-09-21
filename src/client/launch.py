
import wx
from login_dialog import LoginDialog
from document_frame import DocumentFrame

def StartLogin():
    dlg = LoginDialog()
    dlg.ShowModal()
    #dlg.Destroy()  
    

        
def main():
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.

    StartLogin()

    frame = DocumentFrame(None) #wx.Frame(None, wx.ID_ANY, "Your Buisnessgear") # A Frame is a top-level window.
    
    #frame = MainFrame(None, wx.ID_ANY, "Hello!", (50, 50), (600, 400)) 
    #frame.Show()
    app.MainLoop() 
    
if __name__== "__main__":
    main()