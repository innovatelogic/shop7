from xml.dom import minidom
from xml.dom.minidom import *

#----------------------------------------------------------------------------------------------
class CharControlType():
    TEXT        = 1
    COMBOBOX    = 2
    CHECKBOX    = 3

#----------------------------------------------------------------------------------------------
class CharInfo():
    def __init__(self, name, id, type, local = '', opt = None):
        pass 
    
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemController():
    def __init__(self, name):
        self.name = name
        self.characteristics = []
        pass

#----------------------------------------------------------------------------------------------
    def loadXML(self):
        pass

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class ItemControllerHelper():
    TAG_CHAR = "characteristic"
    @staticmethod
    def loadXML(self, filename):
        '''
        @return return ItemController object if load success otherwise None
         '''
        out = None
        
        doc = minidom.parse(filename)
        root_node = doc.getElementsByTagName(TAG_CHAR)[0]
        
        for child in root_node.childNodes:
            pass