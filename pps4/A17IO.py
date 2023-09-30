'''
Created on 6 déc. 2022

@author: garzol
'''
import os
from .register import Register

class A17IO(object):
    '''
    A17IO objects
    '''
    out = 1
    inp = 0

    def __init__(self, id=0):
        '''
        Constructor
        '''
        self.id  = id
        self.oio = Register(16)
        self.iodir = A17IO.inp
        self.tick = 0
        self.fb = list()
        for i in range(16):
            self.fb.append(list())
        self.fdir  = list()
        self.ftick = list()
        
    def stop(self):
        '''
        store in files
        todo later
        '''
        pass
    
    #ret = a170x2.handle(i, cpu.I2.toInt(), ram_addr, cpu.A.toInt())  
    #old call before 2023-09-30          
    #def handle(self, tick, cmd, addr, acc):   
    def handle(self, tick, cpu, addr):   
        self.tick = tick
        #cmd  = Register("{0:08b}".format(cmd))
        cmd  = cpu.I2
        addr = Register("{0:012b}".format(addr))
        #acc  = Register("{0:08b}".format(acc))
        acc  = cpu.A
        ret = None 
        if cmd[4:].toInt() == self.id:
            print("A17", self.id, "received", cmd, addr, acc)
            #provisory the value returned
            #depends on the case whether its input or output 
            #But for now we just get the value of the output buffer
            #2023-09-30 added Register("000")+ to comply with the standard of devices return values
            ret = Register("000")+self.oio[addr[:4].toInt()]
            if cmd.bit(0):
                print("SOS")
                print("IO(", addr[:4], ")<-", acc.bit(3))
                self.oio[addr[:4].toInt()] = '1' if acc.bit(3) else '0'
                
            else:
                print("SES")
             
                if acc.bit(3):
                    print("    Enable all outputs")
                    self.iodir = A17IO.out
                else:
                    print("    Disable all outputs")
                    self.iodir = A17IO.inp
            
        for i in range(16):
            self.fb[i].append(self.oio[i].toInt())    
            #self.fb[i].write("%d"%self.oio[i].toInt()+os.linesep)    
        
        self.fdir.append(self.iodir)
        self.ftick.append(self.tick)   
        return ret
    
    @property
    def id(self):
        return self._id
 
    @id.setter   
    def id(self, id):
        self._id = id
