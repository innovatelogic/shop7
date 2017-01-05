from xml.dom import minidom
from xml.dom.minidom import *

TAG_MAPPING = 'mappings'
TAG_MAP = 'map'
TAG_CATEGORY = 'category'
TAG_ASPECT = "aspect"
TAG_PATH = 'path'

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class BaseMapping():
    def __init__(self, realm):
        self.realm = realm
        self.mapping = []  # [{aspect_name_0: category_id, aspect_name_1: category_id, ...}, ...]
        self.mapping_keys = {}
        pass

#----------------------------------------------------------------------------------------------
    def load(self, filename):
        print('stary load base mapping {}'.format(filename))
        
        doc = minidom.parse(filename)
        root_node = doc.getElementsByTagName(TAG_MAPPING)[0]
        
        for child in root_node.childNodes:
            if child.nodeType == child.ELEMENT_NODE and child.localName == TAG_MAP:
                self.__load_mapping(child)
        print('mapping loaded :{}'.format(len(self.mapping)))

#----------------------------------------------------------------------------------------------
    def __load_mapping(self, node):
        node_mapping = {}
        n_count = 0
        for child in node.childNodes:
            if child.nodeType == child.ELEMENT_NODE and child.localName == TAG_CATEGORY:
                if child.hasAttribute(TAG_ASPECT) and child.hasAttribute(TAG_PATH):
                    aspect = child.getAttribute(TAG_ASPECT)
                    path = child.getAttribute(TAG_PATH)
                    
                    if aspect not in node_mapping:
                        category_node = self.realm.getBaseCategoryByPath(aspect, path.split('%'))
                    
                        if category_node:
                            node_mapping[aspect] = category_node.category._id
                        else:
                            print('mapping failed get category')
                    n_count += 1
                    
        if len(node_mapping) and len(node_mapping) == n_count:
            self.mapping.append(node_mapping)
            
            for key, value in node_mapping.iteritems():
                if key not in self.mapping:
                    self.mapping_keys[key] = {}
                self.mapping_keys[key][str(value)] = self.mapping[len(self.mapping) - 1]
        else:    
            print('error load mapping')
            
#---------------------------------------------------------------------------------------------- 
    def getMapping(self, aspect_id, category_id):
        dict = {}
        if aspect_id in self.mapping_keys:
            if str(category_id) in self.mapping_keys[aspect_id]:
                dict = self.mapping_keys[aspect_id][str(category_id)]
        return dict