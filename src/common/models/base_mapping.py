from xml.dom import minidom
from xml.dom.minidom import *

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class BaseMapping():
    def __init__(self, realm):
        self.realm = realm
        self.mapping = []
        self.mapping_keys = {}
        pass

#----------------------------------------------------------------------------------------------
    def load(self, filename):
        print('base mapping load {}'.format(filename))
        
        doc = minidom.parse(filename)
        root_node = doc.getElementsByTagName("mappings")[0]
        
        for child in root_node.childNodes:
            if child.nodeType == child.ELEMENT_NODE and child.localName == 'map':
                self.__load_mapping(child)
        pass

#----------------------------------------------------------------------------------------------
    def __load_mapping(self, node):
        node_mapping = []
        for child in node.childNodes:
            if child.nodeType == child.ELEMENT_NODE and child.localName == 'category':
                if child.hasAttribute("aspect") and child.hasAttribute('path'):
                    aspect = child.getAttribute("aspect")
                    path = child.getAttribute("path")
                    
                    path_list = path.split('%')
                    category_node = self.realm.getBaseCategoryByPath(aspect, path_list)
                    
                    if category_node:
                        node_mapping.append(category_node.category._id)
                        print('Add mapping {}'.format(category_node.category.name))
                    else:
                        print('mapping failed get category {}'.format(path))
                    
                pass