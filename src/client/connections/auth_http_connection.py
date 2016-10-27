import httplib, urllib

class AuthHTTPConnection:
    def __init__(self, specs):
        self.specs = specs
        self.url = self.specs['auth']['host'] + ':' + self.specs['auth']['port']
        self.connection = None
        
        self.initConnection()
        
    def initConnection(self):
        self.connection = httplib.HTTPConnection(self.url)

    def stopConnection(self):
        self.connection.close()
        
    def request(self, login, password, anonimous):
        params = { 'opcode':'auth', 'login': login, 'password': password, 'anon':anonimous}
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        
        self.connection.request("POST", "/", str(params), headers=headers)
        
        res = self.connection.getresponse()
        
        #print res.status, res.reason
       
        return [res.status == 200, res.read()]