
class CategoryModel():
    class CategoryNode():
        def __init__(self, category):
            self.category = category
            self.childs = []
            
    def __init__(self, db_instance):
        self.db_instance = db_instance
        self.root = None
        self.hashmap = {}
        
    def load(self):
        '''load model from db'''
        print('Load category model')

        self.root = self.CategoryNode(self.db_instance.categories.get_root_category());
        print self.root.category.get()
        self.hashmap[str(self.root.category._id)] = self.root
        
        stack = []
        stack.append(self.root)
        
        count = 0

        while (len(stack) > 0):
            top = stack.pop(0)
            
            childs = self.db_instance.categories.get_childs(top.category)
            count += 1
            
            for child in childs:
                node = self.CategoryNode(child)
                self.hashmap[str(node.category._id)] = node
                top.childs.append(node)
                stack.insert(0, node) 
        
        print('Load category model OK: {} loaded'.format(count))
    
    def save(self):
        pass
    
    #----------------------------------------------------------------------------------------------    
    def get_groups(self, nlvl):
        ''' return categories by id. integer means how levels will return '''
        out = []
        
        max_n = 3 # max depth
        if (nlvl > max_n):
            nlvl = max_n
        
        stack = []
        stack.append(self.root)
        
        while (len(stack) > 0 or nlvl > 0):
            top = stack.pop(0)
            
            out.append({'_id':str(top.category._id), 'parent_id': str(top.category.parent_id), 'name':top.category.name})
            
            childs = top.childs
            nlvl -= 1
            
            for child in childs:
                stack.insert(0, child)
            
        return out

    #----------------------------------------------------------------------------------------------  
    def get_childs(self, str_parent_id):
        out = []
        node = self.hashmap[str_parent_id]
        for child in node.childs:
            out.append({'_id':str(child._id), 'parent_id': str(child.parent_id), 'name':child.name})
        return out