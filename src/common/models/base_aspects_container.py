
class CategoryNode():
    def __init__(self, category):
        self.category = category
        self.childs = []

class Aspect():
    def __init__(self, name, root):
        self.name = name
        self.root = root
        self.hashmap = {}
        if self.root:
            self.hashmap[str(self.root.category._id)] = self.root
        
class BaseAspectsContainer():
    def __init__(self, db_inst):
        self.db_inst = db_inst
        self.aspects = {}
        pass
    
    def load(self):
        self.load_aspect("prom_ua")
        self.load_aspect("amazon")
        self.load_aspect("ebay")
    
    def load_aspect(self, aspect):
        print('Load aspect {}'.format(aspect))
        count = 0
        
        root = CategoryNode(self.db_inst.base_aspects.get_root_category(aspect));
        
        if root.category:
            self.aspects[aspect] = Aspect(aspect, root)
            
            stack = []
            stack.append(self.aspects[aspect].root)
            
            while (len(stack) > 0):
                top = stack.pop(0)
                
                childs = self.db_inst.base_aspects.get_childs(aspect, top.category)
                count += 1

                for child in childs:
                    node = CategoryNode(child)
                    self.aspects[aspect].hashmap[str(node.category._id)] = node
                    top.childs.append(node)
                    stack.insert(0, node) 

        if count == 0:
             print('aspect {} not loaded completely'.format(aspect))
        else:
            print('Load aspect model OK: {} loaded'.format(count))
        
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
    
    def get_aspects(self):
        out = []
        for key in self.aspects:
            out.append(key)
        return out
    
    def get_aspect_category(self, aspect, _id):
        out = None
        if self.aspects.get(aspect):
            if _id in self.aspects[aspect].hashmap:
                out = self.aspects[aspect].hashmap[_id]
        return out
        