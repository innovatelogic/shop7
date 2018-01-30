
import argparse
from auth_server import AuthServer


AUTH_MS_CHANNEL_NAME = 'ms-auth-pipe'

def main():
    print("Auth starting")
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help='server host')
    parser.add_argument('--port', help='server port')
    parser.add_argument('--mshost', type=str, help='master server host')
    parser.add_argument('--ms_auth_queue', type=str, help='master server auth queue name')
    parser.add_argument('--ms_queue_port', type=str, help='master server auth queue port')
    
    args = parser.parse_args()
    
    if not hasattr(args, 'host'):
        raise Exception("Not host argument")
    if not hasattr(args, 'port'):
        raise Exception("Not port argument")
    if not hasattr(args, 'mshost'):
        raise Exception("Not host argument")
    if not hasattr(args, 'ms_auth_queue'):
        raise Exception("Not ms_auth_quevue argument")
    if not hasattr(args, 'ms_queue_port'):
        raise Exception("Not ms_auth_port argument")
     
    specs = dict()
    
    specs['auth_server'] = {
        'host':args.host,
        'port':int(args.port),
        }
    
    specs['ms'] = {
        'host':args.mshost,
        'ms_auth_queue':args.ms_auth_queue,
        'ms_queue_port':int(args.ms_queue_port)
        }
    
    print("Auth init")
    auth_server = AuthServer(specs)

    print("Auth running")
    auth_server.run()
        
    #key = base64.b64encode('guest:guest')
    #run_forever(args.host, int(args.port))
    
if __name__ == '__main__':
    main()
    
    