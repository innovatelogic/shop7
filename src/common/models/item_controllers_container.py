from common.db.types.item_controller import ItemController, ItemControllerHelper
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemControllerContainer():
    def __init__(self, realm, specs):
        self.realm = realm
        self.specs = specs
        self.container = {}
        pass
    
#----------------------------------------------------------------------------------------------
    def loadAll(self):
        aspects = self.realm.base_aspects_container.getAspects()
        
        for aspect in aspects:
            self.__load(aspect)
        
        pass

#----------------------------------------------------------------------------------------------
    def __load(self, aspect):
        
        stack = []
        if aspect:
            stack.append(aspect.root)
            
            while stack:
                top = stack.pop(0)
                
                if top.category.controller_name:
                    print('load controller {}'.format(top.category.controller_name))
                    #filename = ''
                    #top.category.controller_inst = ItemControllerHelper.loadXML()
                
                for child in top.childs:
                    stack.append(child)
            
        pass