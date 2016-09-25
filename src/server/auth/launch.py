import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import sys
import base64
import time
import argparse

key = ""

class AuthHandler(SimpleHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        print "send header"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print "send header"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global key
        ''' Present frontpage with user authentication. '''
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif self.headers.getheader('Authorization') == 'Basic '+key:
            SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            pass
        
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

def test(HandlerClass = AuthHandler, ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)

def run_forever(host_name, port_number):
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((host_name, port_number), AuthHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (host_name, port_number))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
         pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (host_name, port_number)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help='server host')
    parser.add_argument('--port', help='server port')
    
    args = parser.parse_args()
    
    if not hasattr(args, 'host'):
        raise Exception("Not host argument")
    
    if not hasattr(args, 'port'):
        raise Exception("Not port argument")
        
    key = base64.b64encode('guest:guest')
    
    run_forever(args.host, int(args.port))
    
if __name__ == '__main__':
    main()
    
    