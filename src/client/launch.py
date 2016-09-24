
import wx
from login_dialog import LoginDialog
from document_frame import DocumentFrame
import argparse

def StartLogin(specs):
    dlg = LoginDialog(specs)
    dlg.ShowModal()
    #dlg.Destroy()  
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth_host', type=str, help='auth server host')
    parser.add_argument('--auth_port', help='auth server port')
    
    args = parser.parse_args()
    
    if not hasattr(args, 'auth_host'):
        raise Exception("Not auth host argument")
    
    if not hasattr(args, 'auth_port'):
        raise Exception("Not auth port argument")
    
    if not hasattr(args, 'auth_host'):
        raise Exception("Not auth host argument")
    
    if not hasattr(args, 'auth_port'):
        raise Exception("Not auth port argument")
    
    specs = dict()
    
    specs['auth'] = {
        'host':args.auth_host,
        'port':args.auth_port
        }
    
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.

    StartLogin(specs)

    frame = DocumentFrame(None)
    
    app.MainLoop() 
    
if __name__== "__main__":
    main()