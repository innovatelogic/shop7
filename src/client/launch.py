
import wx
import argparse
import time
from threading import Event
from login_dialog import LoginDialog
from document_frame import DocumentFrame
from ms_connection import MSConnection

#----------------------------------------------------------------------------------------------
def StartLogin(specs):
    isLogin = False
    
    dlg = LoginDialog(specs)
    res = dlg.ShowModal()
    
    on_close = dlg.on_close
    
    if dlg.connection_info:
        isLogin = True
    
    dlg.Destroy()  
    return [on_close, isLogin, dlg.connection_info]


#----------------------------------------------------------------------------------------------
def RunClient(app, specs, connection_info):
    
    ready = Event() 
    
    ms_connection = MSConnection(eval(connection_info), ready)
    ms_connection.start()
    
    #block until ready
    ready.wait()
    
    dict = eval(connection_info)

    status = ms_connection.send(str({'opcode': 'auth_activate', 'token':dict['token']}))
    
    if status['res']:
        frame = DocumentFrame(None, dict, ms_connection)
        app.MainLoop() 
    
    ms_connection.stop()

    return DocumentFrame.logout_flag

#----------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth_host', type=str, help='auth server host')
    parser.add_argument('--auth_port', help='auth server port')
    parser.add_argument('--login', type=str, help='default user login')
    parser.add_argument('--password', help='default user pass')    
    
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
    
    def_login = ''
    if hasattr(args, 'login'):
        def_login = args.login
        
    def_pass = ''
    if hasattr(args, 'password'):
        def_pass = args.password
  
    specs['user'] = {
        'login':def_login,
        'pass':def_pass
        }
    
    print(time.asctime(), "Client Starts")
    
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