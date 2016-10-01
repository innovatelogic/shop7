import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import sys
import base64
import time
import argparse
import urlparse
import cgi

from ms_connection import MSConnection

class HTTPAuthHandler(SimpleHTTPRequestHandler):
    def set_ms_connection(self, ms_connection):
        self.ms_connection = ms_connection
     
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        
        dict = eval(post_body)
       
        result = self.ms_connection.send(post_body)
        
        code = 401 #pessimistic by default
        if result:
            code = 200 #processed auth
        
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(result)
        
def MakeHandlerClassFromArgv(ms_connection):
    class CustomHandler(HTTPAuthHandler, object):
        def __init__(self, *args, **kwargs):
            self.set_ms_connection(ms_connection)
            super(CustomHandler, self).__init__(*args, **kwargs)
    return CustomHandler
