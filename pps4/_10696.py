'''
Created on 6 déc. 2022

@author: garzol
'''
import os
from .register import Register

class GPIO10696(object):
    '''
    10696 GPIO objects
    '''
    out = 1
    inp = 0

    def __init__(self, id=0):
        '''
        Constructor
        '''
        self.id  = id
        self.out = Register(12)
        self.inp = Register(12*['1'])
        self.tick = 0
        self.fb = list()
        for i in range(12):
            self.fb.append(list())
        self.ftick = list()
        #     self.fb.append(open("gox{0}_{1:02d}".format(self.id,i), "w"))
        # self.ftick = open("gtick{0}".format(self.id), "w")
        
    def stop(self):
        pass
          
          
    def handle(self, tick, cpu, addr):  
        '''
        addr is not used. Only for standardization with other devices
        ''' 
        self.tick = tick
        cmd  = cpu.I2
        acc  = cpu.A
        ret = None 
        if cmd[4:].toInt() == self.id:
            print("10696", self.id, "received", cmd, acc)
            ret = self.inp[:4]
            if cmd.bit(2): 
                if not cmd.bit(0): 
                    grpstxt = "A"
                    self.out[:4]  = acc
                else:
                    grpstxt = "-"                    
                if not cmd.bit(1): 
                    grpstxt += "B"
                    self.out[4:8] = acc
                else:
                    grpstxt += "-"                    
                if not cmd.bit(3): 
                    grpstxt += "C"
                    self.out[8:]  = acc
                else:
                    grpstxt += "-"                    
                print("SET", grpstxt, "to b{0:04b}".format(acc.toInt()))
                
            else:
                if not cmd.bit(0): 
                    ret = self.inp[:4]
                    grpstxt = "A"
                else:
                    ret = Register(4)
                    grpstxt = "-"                    
                if not cmd.bit(1): 
                    ret = ret or self.inp[4:8]
                    grpstxt += "B"
                else:
                    grpstxt += "-"                    
                if not cmd.bit(3): 
                    ret = ret or self.inp[8:]
                    grpstxt += "C"
                else:
                    grpstxt += "-"  
                print("GET", grpstxt, "value", ret)
                
        for i in range(12):
            self.fb[i].append(self.out[i].toInt())    
        
        self.ftick.append(self.tick)   
        return ret
    
    @property
    def id(self):
        return self._id
 
    @id.setter   
    def id(self, id):
        self._id = id
