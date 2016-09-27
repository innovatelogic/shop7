import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import sys
import base64
import time
import argparse
import urlparse
import cgi

from ms_connection import MSConnection
key = ""

class HTTPAuthHandler(SimpleHTTPRequestHandler):
    def set_ms_connection(self, ms_connection):
        self.ms_connection = ms_connection
        
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

        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        
        dict = eval(post_body)
        
        print str(dict)
        
        self.ms_connection.send(post_body)
            
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

def MakeHandlerClassFromArgv(ms_connection):
    class CustomHandler(HTTPAuthHandler, object):
        def __init__(self, *args, **kwargs):
            self.set_ms_connection(ms_connection)
            super(CustomHandler, self).__init__(*args, **kwargs)
    return CustomHandler
