

class UserSession:
    def __init__(self, token, id, name):
        ''' creates when auth ok'''
        self.activated = False
        self.token = token
        self.id = id
        self.name = name
        pass
    
    def start(self):
        ''' statrs when user connected to master server'''
        pass
    
    def close(self):
        ''' ends when user disconnect from master server'''
        pass