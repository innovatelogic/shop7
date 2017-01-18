from common.db.types.types import ID_NONE

#----------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------- 
class CategoryNode():
    def __init__(self, category, parent):
        self.category = category
        self.parent = parent
        self.controller_inst = None
        self.childs = [] # CategoryNode's
        
    def addChild(self, child_node):
        self.childs.append(child_node)
        
    def getChildByName(self, name):
        out = None
        if self.childs:
            for child in self.childs:
                if child.category.name == name:
                    out = child
                    break
        return out
    
    def setController(self, controller):
        self.controller_inst = controller

    def dump(self, f, deep):
        ''' debug serialize '''
        self.woffset(deep, f)
        f.write(unicode('{} {}'.format(str(self.category.name), self.category._id) + '\n', 'utf8'))
        
        if self.childs:
            for child in self.childs:
                child.dump(f, deep + 1)
            
    def woffset(self, deep, f):
        for x in range(0, deep):
            f.write(unicode('  '))
            
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------   
class Aspect():
    def __init__(self, name, root):
        self.name = name
        self.root = root # CategoryNode
        self.hashmap = {} # id <-> CategoryNode's
        self.foreign_hashmap = {}
        if self.root:
            self.hashmap[str(self.root.category._id)] = self.root
            if self.root.category.foreign_id != ID_NONE:
                self.foreign_hashmap[str(self.root.category.foreign_id)] = self.root
        
    def getCategoryNodeById(self, _id):
        ''' find category with specified _id in tree
        @param _id category id
        @return: Node if found otherwise None
        '''
        out = None
        if str(_id) in self.hashmap:
            out = self.hashmap[str(_id)]
        return out
    
    def getCategoryNodeByForeignId(self, foreign_id):
        ''' find category with specified foreign_id in tree
        @param _id category id
        @return: Node if found otherwise None
        '''
        out = None
        if str(foreign_id) in self.foreign_hashmap:
            out = self.foreign_hashmap[str(foreign_id)]
        return out
    
    def addChild(self, parent_node, child_node):
        parent_node.addChild(child_node)
        self.hashmap[str(child_node.category._id)] = child_node
        if child_node.category.foreign_id != ID_NONE:
            self.foreign_hashmap[str(child_node.category.foreign_id)] = child_node