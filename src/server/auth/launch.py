
import argparse
from auth_server import AuthServer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help='server host')
    parser.add_argument('--port', help='server port')
    
    args = parser.parse_args()
    
    if not hasattr(args, 'host'):
        raise Exception("Not host argument")
    
    if not hasattr(args, 'port'):
        raise Exception("Not port argument")
    
    specs = dict()
    
    specs['auth_server'] = {
        'host':args.host,
        'port':int(args.port)
        }
    
    auth_server = AuthServer(specs)
    auth_server.run()
        
    #key = base64.b64encode('guest:guest')
    #run_forever(args.host, int(args.port))
    
if __name__ == '__main__':
    main()
    
    