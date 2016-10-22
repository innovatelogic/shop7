import time
from user_session import UserSession

USER_TOKEN_START = 456890

class UsersModel():
    def __init__(self, db_instance):
        self.db_instance = db_instance
        self.userSessions = {}
        
        #----------------------------------------------------------------------------------------------
    def authentificateUser(self, login, password):
        loginPass = False
        ausPass = False
        
        print('[authentificateUser]')
        user = self.db_instance.users.get_user_by_name(login)
        
        if user:
            print('[authentificateUser] user ok')
            if user.pwhs == password:
                loginPass = True
        
                user_session = None
                
                _id = user._id
                for key, session in self.userSessions.iteritems():
                    if session.id == _id:
                        user_session = session
                        break
                if user_session == None:
                    user_session = UserSession(++USER_TOKEN_START, user._id, user.name)
                    self.userSessions[user_session.token] = user_session
                    ausPass = True
                else:
                    print(time.asctime(), "user try to %s re-authentificate" % login)
                    ausPass = True
                        
                print(time.asctime(), "user %s authentificate OK" % login)
            else:
                print(time.asctime(), "user %s authentificate FAILED" % login)
        
        return [loginPass and ausPass, user_session]

#----------------------------------------------------------------------------------------------
    def activateUserAuth(self, token):
        out = False
        user_session = self.userSessions[token]
        
        if user_session:
            if not user_session.activated:
                user_session.activated = True
                out = True 
        print(time.asctime(), "user {0} activated {1}".format(user_session.name, str(out)))
        return out

#----------------------------------------------------------------------------------------------
    def logoutUser(self, token):
        out = False
        name = str(token)
        user_session = self.userSessions.get(token)
        if user_session:
            name = user_session.name
            del self.userSessions[token]
            out = True
        print(time.asctime(), "user {0} logout {1}".format(name, str(out)))
        return out