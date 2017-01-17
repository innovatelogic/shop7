from xml.dom import minidom
from xml.dom.minidom import *
from xml.parsers.expat import ExpatError

#----------------------------------------------------------------------------------------------
class CharControlType():
    TEXT        = 1
    COMBOBOX    = 2
    CHECKBOX    = 3

#----------------------------------------------------------------------------------------------
class CharInfo():
    def __init__(self, name, id, type, local = '', opt = ''):
        self.name = name
        self.id = id
        self.type = type
        self.local = local
        self.opt = opt
        pass 
    
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemController():
    TAG_CONTROLLER = "controller"
    TAG_CHAR = "characteristic"
    
    def __init__(self, name):
        self.name = name
        self.characteristics = {}
        pass

#----------------------------------------------------------------------------------------------
    def loadXML(self, filename):
        res = False
        try:
            print('start load controller {}'.format(filename))
            doc = minidom.parse(filename)
            root_node = doc.getElementsByTagName(self.TAG_CONTROLLER)[0]
            
            for child in root_node.childNodes:
                if child.nodeType == child.ELEMENT_NODE and child.localName == self.TAG_CHAR:
                    info = self.__load(child)
                    if info and info.id not in self.characteristics:
                       self.characteristics[info] = info
            print('controller loaded')
            res = True
        except ExpatError as e:
            print(str(e))
            
        return res

#----------------------------------------------------------------------------------------------
    def __load(self, child):
        out = None
        try:
            name = child.getAttribute("name")
            id = child.getAttribute('id')
              
            local = ''
            if child.hasAttribute('local'):
                local = child.getAttribute("local")
                    
            type = ''
            if child.hasAttribute('type'):
                local = child.getAttribute("type")
                
            opt = ''
            if child.hasAttribute('opt'):
                opt = child.getAttribute('opt')
                
            out = CharInfo(name, id, type, local, opt)
            
        except ExpatError as e:
            print(str(e))
        
        return out