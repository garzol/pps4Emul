# pps4Emul
PPS4 instruction set emulator

cpum.py is the main program that executes PPS4 binary program. At point zero the program is preloaded with the gottlieb system 1 exploitation code for testing purposes.


Use testcpu.py to run this program.
PhD 2022-12-06
===


#How to use:

1) create a Pps4Cpu object: 

cpu = Pps4Cpu()


2) create a rom and ram objects:

prom = ROM12(fb) #creation of a rom area from binary file

pram = RAM(256)


3) add devices if you want, for example:

a170x2  = A17IO(0x2)       #

a170x4  = A17IO(0x4)

gpio0x3 = GPIO10696(0xD)

gkpd    = GPKD10788(0xF)


4) create list of devices:

devices = [a170x2, a170x4, gpio0x3, gkpd]

(can be empty: devices = [])


5) you are ready for a system trace:

 #ramv is the value corresponding

 #to the data bus state of the previous cycle

 #at boot up it is not important, but if you trace in 2 successive program calls

 #you will need to put in the 2nd the exact value you had from the last cycle

ramv = 0		
 #you can also set up cpu state:

cpu.P = Register("{0:012b}".format(0x5C0))

cpu.BL = Register("{0:04b}".format(0x2))

 #finally launch trace 	for n cycles 

ncycl = 2000	

cpu.trace(ncycl, prom, pram, devices, ramv)

you may also disassemble the rom, draw graphs, and many things. Read testcpu.py to see all

PhD 2022-12-06
phd@pps4.fr
pps4.fr