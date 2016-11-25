
class CategoryNode():
    def __init__(self, category, parent):
        self.category = category
        self.parent = parent
        self.childs = []

class Aspect():
    def __init__(self, name, root):
        self.name = name
        self.root = root
        self.hashmap = {}
        if self.root:
            self.hashmap[str(self.root.category._id)] = self.root

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------        
class BaseAspectsContainer():
    def __init__(self, db_inst, cache):
        self.db_inst = db_inst
        self.aspects = {}
        self.cache_ref = cache
        pass

#----------------------------------------------------------------------------------------------
    def load(self):
        self.load_aspect("prom_ua")
        #self.load_aspect("amazon")
        self.load_aspect("ebay")

#----------------------------------------------------------------------------------------------
    def load_aspect(self, aspect):
        ''' create category tree'''
        print('Load aspect {}'.format(aspect))
        count = 0
        
        root_node = CategoryNode(self.db_inst.base_aspects.get_root_category(aspect), None);
        
        if root_node.category:
            self.aspects[aspect] = Aspect(aspect, root_node)
            self.cache_ref.add_base_category(aspect, root_node.category._id) #cache
            
            stack = []
            stack.append(root_node)
            
            while (len(stack) > 0):
                top = stack.pop(0)
                
                childs = self.db_inst.base_aspects.get_childs(aspect, top.category)
                count += 1

                for child in childs:
                    node = CategoryNode(child, top)
                    self.aspects[aspect].hashmap[str(node.category._id)] = node
                    self.cache_ref.add_base_category(aspect, node.category._id) #cache
                    
                    top.childs.append(node)
                    stack.insert(0, node) 

        if count == 0:
            print('aspect {} not loaded completely'.format(aspect))
        else:
            print('Load aspect model OK: {} loaded'.format(count))
            
#----------------------------------------------------------------------------------------------
    def get_first_level_categories(self, aspect):
        ''' return categories by id. integer means how levels will return '''
        out = []
        
        if self.aspects.get(aspect):
            
            aspect = self.aspects[aspect]
            out.append({'_id':str(aspect.root.category._id), 
                        'parent_id': str(aspect.root.category.parent_id),
                        'name':aspect.root.category.name, 
                        'n_childs':str(len(aspect.root.childs))})
                
            for item in aspect.root.childs:
                out.append({'_id':str(item.category._id), 
                            'parent_id': str(item.category.parent_id),
                            'name':item.category.name, 
                            'n_childs':str(len(item.childs))})
                
        return out
    
#----------------------------------------------------------------------------------------------
    def get_child_categories(self, aspect, str_parent_id):
        out = []
        if self.aspects.get(aspect):
            aspect = self.aspects[aspect]
            node = aspect.hashmap[str_parent_id]
            for item in node.childs:
                out.append({'_id':str(item.category._id), 
                            'parent_id': str(item.category.parent_id),
                            'name':item.category.name, 
                            'n_childs':str(len(item.childs))})
        return out
    
#----------------------------------------------------------------------------------------------
    def get_aspects(self):
        ''' returns array of loaded aspects'''
        out = []
        for key in self.aspects:
            out.append(key)
        return out
    
#----------------------------------------------------------------------------------------------
    def get_aspect(self, id):
        out = None
        if id in self.aspects:
            out = self.aspects[id]
        return out
    
#----------------------------------------------------------------------------------------------
    def get_aspect_category(self, aspect, _id):
        out = None
        if self.aspects.get(aspect):
            if _id in self.aspects[aspect].hashmap:
                out = self.aspects[aspect].hashmap[_id]
        return out
    
#----------------------------------------------------------------------------------------------
    def get_aspect_category_root(self, aspect):
        out = None
        if aspect in self.aspects:
            out = self.aspects[aspect].root
        return out

#----------------------------------------------------------------------------------------------
    def get_aspect_child_categories(self, aspect, parent_id):
        out = []
        if aspect in self.aspects:
            node = self.aspects[aspect].hashmap[str(parent_id)]
            for item in node.childs:
                out.append(item)
        return out