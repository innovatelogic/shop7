
class CategoryModel():
    
    class CategoryNode():
        def __init__(self, category):
            self.category = category
            self.childs = []
            
    def __init__(self, db_instance):
        self.db_instance = db_instance
        self.root = None
        
    def load(self):
        '''load model from db'''
        print('Load category model')
        
        self.root = self.CategoryNode(self.db_instance.categories.get_root_category());
        
        stack = []
        stack.append(self.root)
        
        count = 0
        
        while (len(stack) > 0):
            top = stack.pop(0)
            
            childs = self.db_instance.categories.get_childs(top.category)
            count += 1
            
            for child in childs:
                node = self.CategoryNode(child)
                top.childs.append(node)
                stack.insert(0, node) 
        
        print('Load category model OK: {} loaded'.format(count))
    
    def save(self):
        pass