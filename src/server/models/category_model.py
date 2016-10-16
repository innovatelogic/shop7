
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
        
        out.append({'_id':str(self.root.category._id), 'parent_id': str(self.root.category.parent_id), 'name':self.root.category.name, 'n_childs':str(len(self.root.childs))})
            
        for item in self.root.childs:
            out.append({'_id':str(item.category._id), 'parent_id': str(item.category.parent_id), 'name':item.category.name, 'n_childs':str(len(item.childs))})
            
        return out
    
    '''    stack = []
        stack.append(self.root)
        
        depth = 0
        while (len(stack) > 0 or depth <= 1):
            
            new_stack = []
            for item in stack:

                out.append({'_id':str(item.category._id), 'parent_id': str(item.category.parent_id), 'name':item.category.name, 'n_childs':str(len(item.childs))})
            
                for child in item.childs:
                    new_stack.append(child)
                
            stack = new_stack
            
            depth += 1
            nlvl -= 1'''

    #----------------------------------------------------------------------------------------------  
    def get_childs(self, str_parent_id):
        out = []
        node = self.hashmap[str_parent_id]
        for item in node.childs:
            out.append({'_id':str(item.category._id), 'parent_id': str(item.category.parent_id), 'name':item.category.name, 'n_childs':str(len(item.childs))})
        return out