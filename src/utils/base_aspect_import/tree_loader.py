from xml.dom import minidom
from xml.dom.minidom import *
import common.db.instance
import common.connection_db
from common.models.base_aspects_container import BaseAspectsContainer, CategoryNode
from common.db.types.types import Category
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class TreeLoader():
    def __init__(self, specs, db):
        self.specs = specs
        self.root = None
        self.db = db
        self.base_aspects_container = BaseAspectsContainer(self.db)
        
#----------------------------------------------------------------------------------------------
    def load(self, filename):
        INVALID_ID = -1
        doc = minidom.parse(filename)
        root_node = doc.getElementsByTagName("node")[0]
        
        self.root = CategoryNode(Category({'_id':INVALID_ID, 'parent_id':None, 'name':'root', 'local':''}), None)
        
        stack = []
        stack.append((root_node, self.root))
        count = 1
        
        while(stack):
            new_stack = []
            for node in stack:
                childs = node[0].childNodes # getElementsByTagName('node')
                
                for child in childs:
                    if child.nodeType == child.ELEMENT_NODE and child.localName == 'node':
                        name = child.getAttribute("name")
                        local = child.getAttribute("local")
                        
                        cat = CategoryNode(Category({'_id':INVALID_ID, 'parent_id':INVALID_ID, 'name':name, 'local':local}), node[1])
                        node[1].childs.append(cat)
                        
                        new_stack.append((child, cat))
                        count += 1
                    
            stack = new_stack
            
        print('processed {} categories'.format(count))
        
        self.base_aspects_container.dump_category_tree(filename + '.tmp2', self.root)
        pass

#----------------------------------------------------------------------------------------------
    def merge(self, source):
        self.base_aspects_container.treeMerge(source, self.root)
        self.base_aspects_container.dump_category_tree(self.specs['path']['data'] + 'merge.tmp', self.root)

#----------------------------------------------------------------------------------------------  
    def save(self, aspect):
        self.base_aspects_container.save_aspect(aspect, self.root)
