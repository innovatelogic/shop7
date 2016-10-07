import io

class CategoryNode():
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self._id = None
        self.parent_id = None
        self.childs = []
        
    def dump(self, f, deep):
        self.woffset(deep, f)
        f.write(unicode(str(self.name) + '\n', 'utf8'))
        
        if self.childs:
            for child in self.childs:
                child.dump(f, deep + 1)
            
    def woffset(self, deep, f):
        for x in range(0, deep):
            f.write(unicode('  '))
            
class CategoryTree():
    def __init__(self):
        self.root = None
        
    def find_by_name(self, name):
        '''find category by name'''
        stack = []
        
        stack.append(self.root)
        
        while (len(stack) > 0):
            top = stack.pop(0)
            
            if (top.name == name):
                return top
            
            for child in top.childs:
                stack.insert(0, child) 

        return None
    
def dump_category_tree(filename, root):
    print("opening damp groups file:" + filename)
    with io.open(filename + '.dump', 'w', encoding='utf8') as f:
        print("opening OK")
        f.write(unicode('{\n'))
        root.dump(f, 0)
        f.write(unicode('}\n'))