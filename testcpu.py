'''
Created on 6 déc. 2022

@author: garzol

start of iol handling
'''
from cProfile import run
import matplotlib.pyplot as plt

from pps4.cpum import ROM12, RAM, Pps4Cpu
from pps4.A17IO import A17IO    
from pps4._10696 import GPIO10696
from pps4._10788 import GPKD10788
from pps4.register import Register
from pps4.cpum import PPS4InstSet

def entryPoint():
    infodict=dict()
    for k,v in PPS4InstSet.HexCod.items():
        for vi in v:
            infodict[vi] = k 
            

    #fb = open("pps4/A1752EFA1753EE.bin", "rb")
    fb = open("pps4/recel_screech.bin", "rb")
    prom = ROM12(fb)  #creation of a rom area from binary file
    fb.close()
    pram = RAM(256)
    cpu = Pps4Cpu()
    
    a170x2  = A17IO(0x2)
    a170x4  = A17IO(0x4)
    gpio0x3 = GPIO10696(0xD)
    gkpd    = GPKD10788(0xF)
    
    # a170x2  = A17IO(0x2)
    # a170x4  = A17IO(0x4)
    # gpio0x3 = GPIO10696(0x3)
    
    devices = [a170x2, a170x4, gpio0x3, gkpd]
    
    if False:
        #this how to access RAM or ROM
        print("===ROM===")
        prom.show(length=10)
        print("===RAM===")  
        pram.show()


    print("===A17 1/switch matrix===")
    print("a17", "id=#{0:01X}".format(a170x2.id))
    
    print("===A17 2/solenoid control===")
    print("a17", "id=#{0:01X}".format(a170x4.id))
    
    print("===CPU===")
    cpu.P = Register("{0:012b}".format(0x005))
    cpu.A = Register("{0:04b}".format(0x0))
    cpu.BL = Register("{0:04b}".format(0x2))
    cpu.BM = Register("{0:04b}".format(0x0))
    cpu.BU = Register("{0:04b}".format(0x0))

    cpu.zapthis = [0x1D2]
    ramv = 0
    cpu.trace(100000, prom, pram, devices, ramv)  

    # for i in range(2000):
    #
    #     ram_addr = (cpu.BL+cpu.BM+cpu.BU).toInt()
    #     rom_addr = cpu.P.toInt()
    #
    #     #cpu.ramd = Register("{0:04b}".format(ramv))
    #     cpu.cyclephi2(ramv)
    #
    #     #print("main: {1}\t{0:04X}\t{2:02X}".format(rom_addr, acc, 0), cpu.P)
    #     romi = prom.mem[rom_addr]
    #
    #     '''
    #     #second half of main cycle (phi3, phi4)
    #     '''
    #     next_ram_addr, ldis, wioioram = cpu.cyclephi4(romi)
    #     wiorw    = cpu.wio
    #
    #     #print("{0:02X}".format(cpu.I1.toInt()), wioioram, wiorw)
    #     if wioioram == Pps4Cpu.ramdev:
    #         ramv = pram.mem[ram_addr]
    #         if wiorw == Pps4Cpu.wr:
    #             print("write:", i, "RAM(@",ram_addr,")<-", cpu.ramout, "next_ram:", next_ram_addr)
    #             pram.mem[ram_addr] = cpu.ramout.toInt()
    #     elif wioioram == Pps4Cpu.iodev:
    #         #print(cpu.A, ram_addr, cpu.I2.toInt())
    #         #print("ioldevice reception of A={0:01X}, B={1:03X}, I2={2:02X}".format(cpu.A.toInt(), ram_addr, cpu.I2.toInt()))
    #         ramviol = None
    #         #def handle(self, tick, cpu, addr):   
    #         ret = a170x2.handle(i, cpu, ram_addr)
    #         if ret is not None:
    #             ramviol = ret.toInt()
    #             #ramviol = 8 if ret == Register('1') else 0
    #             #print("A17 device", a170x2.id, "returned", ramviol)
    #         ret = a170x4.handle(i, cpu, ram_addr)
    #         if ret is not None:
    #             #print("newret", ret)
    #             #ramviol = 8 if ret == Register('1') else 0
    #             #print("A17 device", a170x4.id, "returned", ramviol)
    #             ramviol = ret.toInt()
    #         #ram_addr is not used here
    #         ret = gpio0x3.handle(i, cpu, ram_addr)
    #         if ret is not None:
    #             ramviol = ret.toInt()
    #             #print("10696 device", gpio0x3.id, "returned", ramviol)
    #
    #         #ram_addr is not used here
    #         ret = gkpd.handle(i, cpu, ram_addr)
    #         if ret is not None:
    #             ramviol = ret.toInt()
    #             #print("10788 device", gkpd.id, "returned", ramviol)
    #
    #         if ramviol is not None:
    #             cpu.A = Register("{0:04b}".format(ramviol))
    #     ram_addr = next_ram_addr
    #
    #
    #         # if ldis is not None:
    #         #     if ldis == "":
    #         #         distxt.append(["{0:08d}".format(i), "**********STOP******************", "no infos"])
    #         #         break
    #         #
    #         #     #print("ldis", ldis)  #exemple ldis: ldis ((0, 129, None), 'T\t0001')
    #         #     infos = PPS4InstSet.Doc[infodict[ldis[0][1]]]
    #         #     distxt.append(["{0:08d}".format(i), ldis, infos])
    #         #
    #
    #
    #     if ldis is not None and cpu.skipsubroutine == False and True:
    #         if ldis == "":
    #             print("**********STOP******************", "no infos")
    #             exit(0)
    #         infos = PPS4InstSet.Doc[infodict[ldis[0][1]]]
    #         if ldis[0][2] is not None:
    #             print("{1:08d}\t{2:03X}\t{3:02X}\t{4:02X}\t{5}".format(rom_addr, i, int(ldis[0][0]), int(ldis[0][1]), int(ldis[0][2]), ldis[1]))
    #         else:
    #             print("{1:08d}\t{2:03X}\t{3:02X}\t  \t{4}".format(rom_addr, i, int(ldis[0][0]), int(ldis[0][1]), ldis[1]))
    #
    #     # else:
    #     #     print("{1:08d}\t==============".format(rom_addr, i))

    a170x2.stop()  
    if False:  
        pram.show()
    
    
    
    # print(prom.countinstoccur())   
    #
    #
    # print(a170x2.fb[0])
    # #print(a170x2.fdir)
    # print(a170x2.ftick)
    # print(a170x2.fdir)
 
    fig, ax = plt.subplots()
    #ax.plot(a170x4.ftick, a170x4.fb[0], label="out0")
    #ax.plot(a170x4.ftick, a170x4.fb[1], label="out1")
    ax.plot(a170x2.ftick, a170x2.fb[2], label="out2")
    #ax.plot(a170x2.ftick, a170x2.fb[3], label="out3")
    #ax.plot(a170x2.ftick, a170x2.fdir, label="dir")
    ax.plot(a170x2.ftick, a170x2.fdir, label="dir")
    ax.legend()
    if False:
        plt.show()    
        #print("\t\t{0:04X} {1:02X}".format(ram_addr, ramv))
    # x=Register(b"01000111")
    # y=Register(b"11000111")
    # z=Register(4)
    # print(x&y)
    # try:
    #     print(x&z)
    # except IndexError:
    #     print ("indexerrorpass")
    # try:
    #     print(x&7)
    # except:
    #     print ("indexerrorpass")
    # y.incr()
    # print(x&y)
    # if (x&y).isZero():
    #     print("zero")
    # if (x&Register(8)).isZero():
    #     print("ja voll")
    #
    # if x == y:
    #     print("zobi", x, y, x&y)
    # x=y
    # if x == y:
    #     print("zobi2", x, y, x&y)
    # x=Register(10)
    # if x == Register(9):
    #     print("zarbi")
    # if x<y:
    #     print("caillou")
    # # cpu.P = Register(b"000000111111")
    # # print(cpu.P)
    # # #cpu.P.incr()
    # # cpu.P[0:6].incr()
    # # print(cpu.P)
    # # #cpu.P.incr()
    # # print(cpu.P)
    #
    #
    #######################
    #
    #
    #   disassembly only
    #
    #
    #######################
    if False:
        romdistxt = list()
        cpudis = Pps4Cpu(mode="dasm", ROM=prom.mem)
        romi=0
        rom_addr = 0
        is2cycle = False
        while rom_addr<len(prom.mem):
            romi = prom.mem[rom_addr]
            _, ldis, _ = cpudis.cyclephi4(romi)
            if ldis is not None:
                if ldis == "":
                    romdistxt.append(["**********STOP******************", "no infos"])
                    break
                
                #print("ldis", ldis)  #exemple ldis: ldis ((0, 129, None), 'T\t0001')
                infos = PPS4InstSet.Doc[infodict[ldis[0][1]]]
                if is2cycle:
                    is2cycle = False
                    romdistxt.append([rom_addr-1, ldis, infos])
                else:
                    romdistxt.append([rom_addr, ldis, infos])
    
                rom_addr+=1
            else:
                is2cycle = True
                rom_addr+=1
        
        #exemple of linedis:        
        #[2302, ((2302, 82, 30), 'TL\t21E'), ('Transfer Long', 2, '\n                                 This instruction executes a transfer to any ROM \n                                 word on any page. It occupies two ROM words and \n                                 requires two cycles for execution.\n                                 The first byte loads P(12:9) with field \n                                 I1(4:1) and then the second byte I2(8:1) is\n                                 placed in P(8:1)\n                                 ', '\n                                 N/A\n                                 ', 'P(12:9)<-I1(4:1)\nP(8:1)<-I2(8:1)')]
    
        for linedis in romdistxt:
            #print(linedis)
            print("{0:03X}".format(linedis[1][0][0]), end='\t')
            print("{0:02X}".format(linedis[1][0][1]), end='\t')
            try:
                print("{0:02X}".format(linedis[1][0][2]), end='\t')
            except:
                print('  ', end='\t')
            if len(linedis[1][1])>20:
                print(linedis[1][1], end='\t')
            elif len(linedis[1][1])<4:
                print(linedis[1][1], end='\t\t\t\t\t')
            else:
                print(linedis[1][1], end='\t\t\t\t')
            print(";", linedis[2][0])
            
            
            
if __name__ == '__main__':
    entryPoint()
    #run('''entryPoint()''')
    

            