from common.db.types.item_controller import ItemController

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
                
                if top.category.controller:
                    filename = self.specs['path']['data_dir'] +'controllers/' + top.category.controller
                    
                    ctrl = ItemController(top.category.controller)
                    if ctrl.loadXML(filename):
                        top.category.controller_inst = ctrl
                
                for child in top.childs:
                    stack.append(child)
        pass