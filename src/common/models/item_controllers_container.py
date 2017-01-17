from common.db.types.item_controller import ItemController

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemControllerContainer():
    def __init__(self, realm, specs):
        self.realm = realm
        self.specs = specs
        self.container = {}
        self.default_controller = ItemController('default')
        self.default_controller.loadXML(self.specs['path']['data_dir'] +'controllers/default.xml')
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
                    if top.category.controller not in self.container:
                        filename = self.specs['path']['data_dir'] +'controllers/' + top.category.controller
                        ctrl = ItemController(top.category.controller)
                        if ctrl.loadXML(filename):
                            top.category.controller_inst = ctrl
                            self.container[top.category.controller] = ctrl
                    else:
                        top.category.controller_inst = self.container[top.category.controller]
                    
                for child in top.childs:
                    stack.append(child)
        pass