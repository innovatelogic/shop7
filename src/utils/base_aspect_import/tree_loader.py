from xml.dom import minidom
from xml.dom.minidom import *
from common.categories_tree import CategoryTree, CategoryNode
import common.connection_db

class TreeLoader():
    def __init__(self):
        self.tree = CategoryTree()
        self.tree.root = CategoryNode('root', 0)
        
    def load(self, filename):
        print filename
        
        doc = minidom.parse(filename)
        root_node = doc.getElementsByTagName("node")[0]
        
        stack = []
        stack.append((root_node, self.tree.root))
        count = 1
        
        while(stack):
            new_stack = []
            for node in stack:
                childs = node[0].getElementsByTagName('node')
                
                for child in childs:
                    name = child.getAttribute("name")
                    local = child.getAttribute("local")
                    
                    cat = CategoryNode(name, None, local)
                    node[1].childs.append(cat)
                    
                    new_stack.append((child, cat))
                    count += 1
                    
            stack = new_stack
            
        print('processed {} categories'.format(count))
        #common.categories_tree.dump_category_tree(filename + '.tmp', self.tree.root)
        pass