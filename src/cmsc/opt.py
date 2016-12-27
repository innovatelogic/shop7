
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class variant():
    def __init__(self, key, desc, func = None, params = None):
        self.key = key
        self.desc = desc
        self.func = func
        self.params = params
        
    def prnt(self):
        print('{} - {}'.format(self.key, self.desc))
    
    def run(self):
        res = 1
        if self.func:
            res = self.func(self.params)
        return res
    
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class Opt():
    ''' options incapsulator opt input {'str(option)': (str(desc), func, params), ... } '''
    def __init__(self, opt):
        self.opt = opt
        
    def optPrint(self):
        print('>>')
        for opt in self.opt:
            opt.prnt()
        print('q - quit')
        
    def run(self):
        while(True):
            self.optPrint()
            flag = False
            line = raw_input().strip().lower()
            for opt in self.opt:
                if line == opt.key:
                    if opt.run() == 1:
                        return
                    flag = True
                    
            if line == 'q':
                break
            
            if not flag:
                print('invalid input')
    
    @staticmethod
    def input():
        return raw_input().strip().lower()