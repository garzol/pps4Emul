'''
Created on 6 déc. 2022

@author: garzol
'''
from .register import Register

class GPKD10788(object):
    '''
    
    '''
    cod = {
        Register(b"1100").toInt() : "KTR",
        Register(b"1010").toInt() : "KTS",
        Register(b"1110").toInt() : "KLA",
        Register(b"1101").toInt() : "KLB",
        Register(b"0011").toInt() : "KDN",
        Register(b"1011").toInt() : "KAF",
        Register(b"0111").toInt() : "KBF",
        Register(b"0110").toInt() : "KER",
        }

    def __init__(self, id=0):
        '''
        Constructor
        '''
        self.name = "10788"
        self.id  = id
        self.regA = 16*[Register(4)]
        self.regB = 16*[Register(4)]
        self.out = Register(12)
        self.inp = Register(12*['1'])
        self.tick = 0
        self.bookkeeping = list()
        
    def stop(self):
        pass
                
    def handle(self, tick, cpu, addr):  
        '''
        addr is not used here
        ''' 
        self.tick = tick
        cmd  = cpu.I2
        acc  = cpu.A
        bl   = cpu.BL 
        bm   = cpu.BM
        #acc  = Register("{0:08b}".format(acc))
        ret = None 
        if cmd[4:].toInt() == self.id:
            if cmd[:4] == Register(b"1110"): #KLA
                self.regA.insert(0, acc)
                self.regA.pop()
            if cmd[:4] == Register(b"1101"): #KLB
                self.regB.insert(0, acc)
                self.regB.pop()
            try:
                tcmd = GPKD10788.cod[cmd[:4].toInt()]
                self.bookkeeping.append( (tick, tcmd, cmd, acc, "{0:02X}".format((bl+bm).toInt())) )
            except:
                print("problemo==========")
                self.bookkeeping.append( (tick, "problemo", cmd, acc, "{0:02X}".format((bl+bm).toInt())) )
            ret = acc
        return ret

    def graph(self):
        return [], []        

    def printbook(self):
        for elem in self.bookkeeping:
            print(elem)
