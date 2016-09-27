import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import base64
import time

from http_auth_handler import HTTPAuthHandler, MakeHandlerClassFromArgv
from ms_connection import MSConnection

class AuthServer:
    def __init__(self, specs):
        self.specs = specs
        self.ms_connection = MSConnection(specs)
    
    def run(self):
        host_name = self.specs['auth_server']['host']
        port_number = self.specs['auth_server']['port']
        
        self.ms_connection.start()
        
        server_class = BaseHTTPServer.HTTPServer
        HandlerClass = MakeHandlerClassFromArgv(self.ms_connection)

        httpd = server_class((host_name, port_number), HandlerClass)
        
        print(time.asctime(), "Auth Server Starts - %s:%s" % (host_name, port_number))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
             pass
        httpd.server_close()
        print time.asctime(), "Auth Server Stops - %s:%s" % (host_name, port_number)
        
        self.ms_connection.stop()
        pass