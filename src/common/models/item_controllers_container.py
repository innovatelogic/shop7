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
        aspect = self.realm.base_aspects_container.getAspect('basic')
        self.__load(aspect)
        pass

#----------------------------------------------------------------------------------------------
    def __load(self, aspect):
        ''' iterate through aspect and load all aspects'''
        stack = []
        if aspect:
            stack.append(aspect.root)
            
            while stack:
                top = stack.pop(0)
                
                name = top.category.controller
                if name:
                    if name not in self.container:
                        filename = self.specs['path']['data_dir'] +'controllers/' + name
                        ctrl = ItemController(name)
                        if ctrl.loadXML(filename):
                            top.setController(ctrl)
                            self.container[name] = ctrl
                        else:
                            print('fail load {}'.format(filename))
                    else:
                        top.category.controller_inst = self.container[top.category.controller]
                    
                for child in top.childs:
                    stack.append(child)
        pass
    
#----------------------------------------------------------------------------------------------
    def getBasicAspectCategoryController(self, category_id):
        ''' return category's controller. otherwise default '''
        out = self.default_controller.desc()
        aspect = self.realm.base_aspects_container.getAspect('basic')
        if aspect:
            category_node = aspect.getCategoryNodeById(category_id)
            if category_node:
                top = category_node
                while top:
                    if top.controller_inst:
                        out = top.controller_inst.desc()
                        break
                    top = top.parent
            else:
                print('[getBasicAspectCategoryController] find category {} fail '.format(category_id))
        else:
            print('[getBasicAspectCategoryController] find aspect basic fail ')
        return out