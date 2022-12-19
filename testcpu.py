'''
Created on 6 déc. 2022

@author: garzol

start of iol handling
'''
from pps4.cpum import ROM12, RAM, Pps4Cpu
from pps4.A17IO import A17IO    
from pps4._10696 import GPIO10696
from pps4.register import Register
from pps4.cpum import PPS4InstSet

if __name__ == '__main__':
    infodict=dict()
    for k,v in PPS4InstSet.HexCod.items():
        for vi in v:
            infodict[vi] = k 
            

    fb = open("pps4/A1752EFA1753EE.bin", "rb")
    prom = ROM12(fb)  
    fb.close()
    pram = RAM(256)
    cpu = Pps4Cpu()
    a170x2  = A17IO(0x2)
    a170x4  = A17IO(0x4)
    gpio0x3 = GPIO10696(0x3)
    print("===ROM===")
    prom.show(length=10)
    print("===RAM===")  
    pram.show()


    print("===A17 switch matrix===")
    print("a17", "id=#{0:01X}".format(a170x2.id))
    
    print("===A17 solenoid control===")
    print("a17", "id=#{0:01X}".format(a170x4.id))
    
    print("===CPU===")
    ramv = 0
    for i in range(20000):
        
        '''
        #first half of main cycle (phi1, phi2)
        #during phi2, cpu push ROM address on the bus
        '''
        acc, rom_addr, wiorw = cpu.cyclephi12(ramv)
        romi = prom.mem[rom_addr]
        #print("main: {1:08d}\t{0:04X}\t{2:02X}".format(rom_addr, i, romi))
        
        '''
        #second half of main cycle (phi3, phi4)
        '''
        ram_addr, ldis, wioioram = cpu.cyclephi34(romi)
        
        #print("{0:02X}".format(cpu.I1.toInt()), wioioram, wiorw)
        if wioioram == Pps4Cpu.ramdev:
            ramv = pram.mem[ram_addr]
            if wiorw == Pps4Cpu.wr:
                #print("write:", acc, ram_addr)
                pram.mem[ram_addr] = acc
        elif wioioram == Pps4Cpu.iodev:
            #print(cpu.A, ram_addr, cpu.I2.toInt())
            #print("ioldevice reception of A={0:01X}, B={1:03X}, I2={2:02X}".format(cpu.A.toInt(), ram_addr, cpu.I2.toInt()))
            ret = a170x2.handle(i, cpu.I2.toInt(), ram_addr, cpu.A.toInt())
            if ret is not None:
                ramv = 8 if ret == Register('1') else 0
                print("A17 device", a170x2.id, "returned", ramv)
            ret = a170x4.handle(i, cpu.I2.toInt(), ram_addr, cpu.A.toInt())
            if ret is not None:
                ramv = 8 if ret == Register('1') else 0
                print("A17 device", a170x4.id, "returned", ramv)
            ret = gpio0x3.handle(i, cpu.I2.toInt(), cpu.A.toInt())
 
  
            # if ldis is not None:
            #     if ldis == "":
            #         distxt.append(["{0:08d}".format(i), "**********STOP******************", "no infos"])
            #         break
            #
            #     #print("ldis", ldis)  #exemple ldis: ldis ((0, 129, None), 'T\t0001')
            #     infos = PPS4InstSet.Doc[infodict[ldis[0][1]]]
            #     distxt.append(["{0:08d}".format(i), ldis, infos])
            #

        
        if ldis is not None:
            if ldis == "":
                print("**********STOP******************", "no infos")
                exit(0)
            infos = PPS4InstSet.Doc[infodict[ldis[0][1]]]
            if ldis[0][2] is not None:
                print("{1:08d}\t{2:03X}\t{3:02X}\t{4:02X}\t{5}".format(rom_addr, i, int(ldis[0][0]), int(ldis[0][1]), int(ldis[0][2]), ldis[1]))
            else:
                print("{1:08d}\t{2:03X}\t{3:02X}\t  \t{4}".format(rom_addr, i, int(ldis[0][0]), int(ldis[0][1]), ldis[1]))
                
        # else:
        #     print("{1:08d}\t==============".format(rom_addr, i))

    a170x2.stop()    
    pram.show()
    print(prom.countinstoccur())        
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
    print("-----Achtung----------")
    # cpu = Pps4Cpu(mode="dasm")
    # i=0
    # romi=0
    # rom_addr = 0
    # while rom_addr<len(prom.mem):
    #     romi = prom.mem[rom_addr]
    #     _, ldis, _ = cpu.cyclephi34(romi)
    #     if ldis is not None:
    #         print("main: {1:08d}\t{0:04X}\t{2:02X}\t{3}".format(rom_addr, i, cpu.P.toInt(), ldis))
    #     i+=1
    #     rom_addr+= 1

