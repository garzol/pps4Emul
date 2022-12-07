'''
Created on 6 déc. 2022

@author: garzol
'''
from pps4.cpum import ROM12, RAM, Pps4Cpu


if __name__ == '__main__':
    fb = open("pps4/A1752EFA1753EE.bin", "rb")
    prom = ROM12(fb)  
    fb.close()
    pram = RAM(256)
    cpu = Pps4Cpu()
    print("===ROM===")
    prom.show(length=10)
    print("===RAM===")
    pram.show()
    print("===CPU===")
    ramv = 0
    for i in range(8192):
        acc, rom_addr, wio = cpu.cyclephi12(ramv)
        romi = prom.mem[rom_addr]
        #print("main: {1:08d}\t{0:04X}\t{2:02X}".format(rom_addr, i, romi))
        ram_addr, ldis = cpu.cyclephi34(romi)
        #print(cpu.I1, cpu.skipNext, "cpu.skipNext")
        ramv = pram.mem[ram_addr]
        if wio == Pps4Cpu.wr:
            #print("write:", acc, ram_addr)
            pram.mem[ram_addr] = acc
        if ldis is not None:
            if ldis == "":
                print("**********STOP******************")
                exit(0)
            print("{1:08d}\t{2}".format(rom_addr, i, ldis))
        # else:
        #     print("{1:08d}\t==============".format(rom_addr, i))
        
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

