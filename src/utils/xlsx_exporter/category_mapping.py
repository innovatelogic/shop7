import codecs, json, io

class CategoryMapping():
    def __init__(self, specs):
        self.specs = specs
        self.mapping = {}
        
    def init(self):
        self.mapping = {}
        self.loadItems(self.specs['path']['out'] + self.specs['path']['mapping'])
        
    def loadItems(self, filename):
        print ('opening mapping file:' + filename)
        with io.open(filename, 'r', encoding = 'utf8') as f:
            print 'opening OK'
            for line in f:
                print line
                row = json.loads(line.encode('ascii', 'ignore'))
                print row
                self.mapping[row['id_val']] = row['id_key'] # for farst search swap key-val
        return self.mapping
    
    def get_category(self, id):
        if id in self.mapping:
            return self.mapping(id)
        return None