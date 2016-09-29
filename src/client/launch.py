
import wx
from login_dialog import LoginDialog
from document_frame import DocumentFrame
import argparse

def StartLogin(specs):
    isLogin = False
    
    dlg = LoginDialog(specs)
    res = dlg.ShowModal()
    
    on_close = dlg.on_close
    
    if dlg.connection_info:
        isLogin = True
    
    dlg.Destroy()  
    return [on_close, isLogin, dlg.connection_info]


def RunClient(app, specs, connection_info):
    frame = DocumentFrame(None, connection_info)
    app.MainLoop() 
    return DocumentFrame.logout_flag

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth_host', type=str, help='auth server host')
    parser.add_argument('--auth_port', help='auth server port')
    
    args = parser.parse_args()
    
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

    while True:
        on_close, isLogin, connection_info = StartLogin(specs)
        
        if isLogin:
            if not RunClient(app, specs, connection_info):
                break
            continue
        
        if on_close:
            break
    
if __name__== "__main__":
    main()