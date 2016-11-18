import time
from user_session import UserSession
from groups_model import GroupsModel

USER_TOKEN_START = 456890

class UsersModel():
    def __init__(self, db_instance, groups_model):
        self.db_instance = db_instance
        self.userSessions = {}
        self.groupSessions = {}
        self.groups_model = groups_model
        
#----------------------------------------------------------------------------------------------
    def authentificateUser(self, login, password):
        '''comes from http request'''
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
                    self.groups_model.loadUserGroupSession(user.group_id, USER_TOKEN_START)
                    
                    ausPass = True
                else:
                    print(time.asctime(), "user try to %s re-authentificate" % login)
                    ausPass = True
                        
                print(time.asctime(), "user %s authentificate OK" % login)
            else:
                print(time.asctime(), "user %s authentificate FAILED" % login)
        
        return [loginPass and ausPass, user_session]
    
#----------------------------------------------------------------------------------------------
    def get_group_id_by_token(self, token):
        if self.userSessions.get(token):
            return self.userSessions[token].group_id
        return -1
    
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
            self.groups_model.releaseUserGroupSession(USER_TOKEN_START)
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

#----------------------------------------------------------------------------------------------        
    def get_first_level_categories(self, token):
        return self.groups_model.get_first_level_categories(self.get_group_id_by_token(token))

#----------------------------------------------------------------------------------------------  
    def get_child_categories(self, token, _id):
        return self.groups_model.get_child_categories(self.get_group_id_by_token(token), _id)
    
#----------------------------------------------------------------------------------------------    
    def get_user_settings(self, token):
        user_session = self.userSessions.get(token)
        if user_session:
            return user_session.settings;
        return None