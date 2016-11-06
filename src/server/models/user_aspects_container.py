
from bson.objectid import ObjectId
from common.db.types.types import Category, UserAspect, User

class UserAspectsContainer():
    def __init__(self, db_inst):
        self.db_inst = db_inst
        self.activeUserAspects={}
        pass
    
    def loadUserAspect(self, group_id):
        pass
    
    def unloadUserAspect(self):
        pass
    
    def createUserAspect(self, group_id):
        '''creates default user aspect'''
        root_category =  Category({'_id': ObjectId(), 'parent_id': None, 'name':'root'})
        root_node = UserAspect.Node(root_category)
        
        all_category =  Category({'_id': ObjectId(), 'parent_id': root_category._id, 'name':'All'})
        all_node = UserAspect.Node(all_category)
        
        root_node.childs.append(all_node)
        
        user_aspect = UserAspect({'_id':ObjectId(), 'group_id':group_id, 'node_root':root_node})
        
        self.db_inst.user_aspects.add_aspect(user_aspect)