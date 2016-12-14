from xml.dom.minidom import *

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class BaseFileReader():
    def __init__(self, specs):
        self.specs = specs
        self.doc = Document()
        self.root = self.doc.createElement('node')
        self.root.setAttribute("name", "root")
        
        self.doc.appendChild(self.root)
        pass

#----------------------------------------------------------------------------------------------
    def read(self):
        file = self.specs['path']['data'] + self.specs['path']['filename']
        print('read {}'.format(file))
        with open(file) as f:
            data = f.readlines()
            for line in data:
                self.addXML(line)
                
#----------------------------------------------------------------------------------------------
    def addXML(self, line):
        print(line)
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        line = line.strip(' ')
        
        words = line.split("/")
        node_to_add = self.root
        for word in words:
            node_to_add = self.pushNode(node_to_add, word)
            
#----------------------------------------------------------------------------------------------        
    def pushNode(self, node, name):
        childs = node.getElementsByTagName('node')
        for child in childs:
            if child.getAttribute('name') == name:
                return child

        new_node = self.doc.createElement('node')
        new_node.setAttribute("name", name)
        new_node.setAttribute("local", "")
        node.appendChild(new_node)
        return new_node
        
#----------------------------------------------------------------------------------------------
    def save(self, filename):
        out = self.specs['path']['out'] + filename
        print('save to {}'.format(out))
        self.doc.writexml(open(out, 'w'),
                       indent=" ",
                       addindent= "    ",
                       newl='\n')