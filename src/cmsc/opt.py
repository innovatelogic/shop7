
#----------------------------------------------------------------------------------------------
class Opt():
    ''' options incapsulator opt input {'str(option)': (str(desc), func, params), ... } '''
    def __init__(self, opt):
        self.opt = opt
        
    def optPrint(self):
        print('>>')
        for key, value in self.opt.iteritems():
            print('{} - {}'.format(key, value[0]))
        print('q - quit')
        
    def run(self):
        while(True):
            self.optPrint()
            flag = False
            line = raw_input().strip().lower()
            for key, value in self.opt.iteritems():
                if line == key:
                    if value[1]:
                        if value[1](value[2]) == 1: 
                            return
                    else:
                        print('invalid operation')
                    flag = True
                    
            if line == 'q':
                break
            
            if not flag:
                print('invalid input')
    
    @staticmethod
    def input():
        return raw_input().strip().lower()