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
        file = self.specs['path']['data'] + 'base_aspect.txt'#self.specs['path']['filename']
        print('read {}'.format(file))
        count = 0
        with open(file) as f:
            data = f.readlines()
            for line in data:
                self.addXML(line)
                count += 1
                
        print('read {} lines'.format(count))

#----------------------------------------------------------------------------------------------
    def addXML(self, line):
        #print(line)
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        line = line.strip(' ')
        
        words = line.split("/")
        node_to_add = self.root
        bAdded = False
        
        for word in words:
            #print word
            bAdd = True
            childs = node_to_add.childNodes # getElementsByTagName('node')
            for child in childs:
                if child.nodeType == child.ELEMENT_NODE and child.localName == 'node':
                    if child.getAttribute("name") == word:
                        node_to_add = child
                        bAdd = False
                        break
                        
            if bAdd:
                self.pushNode(node_to_add, word)
                bAdded = True
                
        if not bAdded:
            print('ignore {}'.format(line))
            
#----------------------------------------------------------------------------------------------
    def pushNode(self, node, name):
        new_node = self.doc.createElement('node')
        new_node.setAttribute("name", name)
        new_node.setAttribute("local", "")
        new_node.setAttribute("foreign_id", "")
        node.appendChild(new_node)

#----------------------------------------------------------------------------------------------
    def save(self, filename):
        out = self.specs['path']['out'] + filename
        print('save to {}'.format(out))
        self.doc.writexml(open(out, 'w'),
                       indent=" ",
                       addindent= "    ",
                       newl='\n')