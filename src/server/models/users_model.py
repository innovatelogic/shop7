import time
from user_session import UserSession
from groups_model import GroupsModel

USER_TOKEN_START = 456890

class UsersModel():
    def __init__(self, db_instance):
        self.db_instance = db_instance
        self.userSessions = {}
        self.groupSessions = {}
        self.groupsModel = GroupsModel(db_instance)
        
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
                    ++USER_TOKEN_START
                    user_session = UserSession(USER_TOKEN_START, user._id, user.name, user.group_id)
                    self.userSessions[USER_TOKEN_START] = user_session
                    
                    #cache group info
                    self.groupsModel.loadUserGroupSession(user.group_id, USER_TOKEN_START)
                    
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
            
            #release group info
            self.groupsModel.releaseUserGroupSession(USER_TOKEN_START)
            
            out = True
        print(time.asctime(), "user {0} logout {1}".format(name, str(out)))
        return out

#---------------------------------------------------------------------------------------------- 
    def createUser(self, rights, group_id = None):
        '''creates user with all facility or attach to group [group_id] '''
        pass
    
#----------------------------------------------------------------------------------------------     
    def deleteUser(self, id):
        '''delete user. if user last in group delete all aditional facility (group, items, mapping, aspect)'''
        pass
    
#----------------------------------------------------------------------------------------------         
    def updateUser(self, spec):
        '''update user. 
        TODO spec doc.
        '''
        pass