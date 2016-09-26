import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import base64
import time

from http_auth_handler import HTTPAuthHandler 

class AuthServer:
    def __init__(self, specs):
        self.specs = specs
    
    def run(self):
        host_name = self.specs['auth_server']['host']
        port_number = self.specs['auth_server']['port']
        
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((host_name, port_number), HTTPAuthHandler)
        print(time.asctime(), "Server Starts - %s:%s" % (host_name, port_number))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
             pass
        httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (host_name, port_number)
        pass