'''
Created on 26 nov. 2022

@author: garzol

IOL is done
'''
import random
from .register import Register

class PPS4InstSet():
    '''
    Doc is integrally copied from the original datasheet
    
    dictionary such as:
    keycode:("instruction name", #cycle, "Description", "exceptions", "equation")
    ''' 
    HexCod = {
        "LBL":  [0x00],
        "TML":  [0x01, 0x02, 0x03],
        "LBUA": [0x04],
        "RTN":  [0x05],
        "XS":   [0x06],
        "RTNSK":[0x07],
        "ADCSK":[0x08],
        "ADSK": [0x09],
        "ADC":  [0x0A],
        "AD":   [0x0B],
        "EOR":  [0x0C],
        "AND":  [0x0D],
        "COMP": [0x0E],
        "OR":   [0x0F],
        "LBMX": [0x10],
        "LABL": [0x11],
        "LAX":  [0x12],
        "SAG":  [0x13],
        "SKF2": [0x14],
        "SKC":  [0x15],
        "SKF1": [0x16],
        "INCB": [0x17],
        "XBMX": [0x18],
        "XABL": [0x19],
        "XAX":  [0x1A],
        "LXA":  [0x1B],
        "IOL":  [0x1C],
        "DOA":  [0x1D],
        "SKZ":  [0x1E],
        "DECB": [0x1F],
        "SC":   [0x20],
        "SF2":  [0x21],
        "SF1":  [0x22],
        "DIB":  [0x23],
        "RC":   [0x24],
        "RF2":  [0x25],
        "RF1":  [0x26],
        "DIA":  [0x27],
        "EXD":  [x for x in range(0x28,0x30)],
        "LD":   [x for x in range(0x30,0x38)],
        "EX":   [x for x in range(0x38,0x40)],
        "SKBI": [x for x in range(0x40,0x50)],
        "TL":   [x for x in range(0x50,0x60)],
        "ADI":  [x for x in range(0x60,0x65)]+[x for x in range(0x66,0x6F)],
        "DC":   [0x65],
        "CYS":  [0x6F],
        "LDI":  [x for x in range(0x70,0x80)],
        "T":    [x for x in range(0x80,0xC0)],
        "LB":   [x for x in range(0xC0,0xD0)],
        "TM":   [x for x in range(0xD0,0x100)],
        
        }
    Doc = {
        "LB":    ("Load B Indirect", 2,     '''
                                         Sixteen consecutive locations on ROM
                                         page 3 (I2) contain data which
                                         can be loaded into the eight
                                         least significant bits of the B
                                         register by use of any LB instruction.
                                         The four most significant bits of B register
                                         will be loaded with zeroes.
                                         The contents of the SB register will be
                                         destroyed. This instruction takes two
                                         cycles to execute but occupies only one ROM
                                         word. (Automatic return)
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "SB<-SA\nSA<-P\nP(12:5)<-00001100\nP(4:1)<-I1(4:1)\nBU<-0000\nB(8:1)<-|I2(8:1)|\nP<-SA\nSA<->SB"),
                             
        "LBL":    ("Load B Long", 2,     '''
                                         This instruction occupies two ROM words,
                                         the second of which will be loaded
                                         into the eight least significant
                                         bits of the B register.
                                         The four most significant bits of B (BU)
                                         will be loaded with zeroes.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "BU<-0000\nB(8:1)<-|I2(8:1)|"),
        
         "CYS":    ("Cycle SA register and Accumulator", 1,  '''
                                         A 4-bit right shift of the SA
                                         register takes place with the four 
                                         bits which are shifted off the end of SA 
                                         being transferred into the accumulator.
                                         The contents of the accumulator are 
                                         placed in the left end of SA register. 
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-SA(4:1)\nSA(4:1)<-SA(8:5)\nSA(8:5)<-SA(12:9)\nSA(12:9)<-A"),
         
         "SAG":    ("Special Address Generation", 1,  '''
                                         This instruction causes the eight most 
                                         significant bits of the RAM address output 
                                         to be zeroed during the next cycle only. 
                                         Note that this instruction does not 
                                         alter the contents of the B register. 
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "A/B Bus(12:5)<-0000 0000\nA/B Bus(4:1)<-BL(4:1)\nContents of 'B' remain unchanged"),
         
         "LABL":    ("Load Accumulator with BL", 1,  '''
                                         The contents of BL register are 
                                         transferred to the Accumulator.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-BL"),
         
         "LD":    ("Load Accumulator from Memory", 1,  '''
                                         The 4-bit contents of RAM currently 
                                         addressed by B register are placed in 
                                         the accumulator. The RAM address in 
                                         the B register is then modified 
                                         by the result of an exclusive OR 
                                         of the 3-bit immediate field 
                                         I(3:1) and B(7:5).
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-M\nB(7:5)<-B(7:5)xor|I(3:1)|"),
         
         "INCB":    ("Increment BL", 1,  '''
                                         BL register (least significant four bits of B register)
                                         is incremented by 1. If the new contents of BL
                                         is 0000, then the next ROM word will be ignored.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "BL<-BL+1\nSkip on BL=0000"),
                             
         "DECB":    ("Decrement BL", 1,  '''
                                         BL register (least significant four bits of B register)
                                         is decremented by 1. If the new contents of BL
                                         is 1111, then the next ROM word will be ignored.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "BL<-BL-1\nSkip on BL=1111"),
                             
         "RTN":    ("Return", 1,         '''
                                         This instruction executes a return 
                                         from subroutine by loading contents of 
                                         SA register into P register and interchange 
                                         the SB and SA registers.                                         
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "P<-SA\nSA<->SB"),
                             
         "RTNSK":    ("Return and Skip", 1,         '''
                                         Same as RTN except the first ROM
                                         word encountered after the return 
                                         from subroutine is skipped.                                       
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "P<-SA\nSA<->SB\nP<-P+1"),
                             
         "XS":    ("Exchange SA and SB", 1,  '''
                                         The 12-bit contents of SA register and SB 
                                         register are exchanged
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "SA<->SB"),
                             
         "AD":    ("Add", 1,  '''
                              The result of binary addition 
                              of contents of accumulator 
                              and 4-bit contents of the RAM currently 
                              addressed by B register, replaces the 
                              contents of accumulator. The resulting 
                              carry-out is loaded into C flip-flop.
                              ''',
                                 '''
                                 N/A
                                 ''',
                                 "C,A<-A+M"),
                             
         "ADC":    ("Add with carry-in", 1,  '''
                              Same as AD except the 
                              C flip-flop serves as a carry-in 
                              to the adder.
                              ''',
                                 '''
                                 N/A
                                 ''',
                                 "C,A<-A+M+C"),
            
         "ADCSK":    ("Add with carry-in and skip on carry-out", 1,  '''
                              Same as ADSK except the 
                              C flip-flop serves as a carry-in 
                              to the adder.
                              ''',
                                 '''
                                 N/A
                                 ''',
                                 "C,A<-A+M+C\nSkip if C=1"),
            
         "ADSK":    ("Add and skip on carry-out", 1,  '''
                              Same as AD except the next ROM word 
                              will be skipped (ignored) if
                              a carry-out is generated.
                              ''',
                                 '''
                                 N/A
                                 ''',
                                 "C,A<-A+M\nSkip if C=1"),
            
           
         "AND":    ("Logical AND", 1,  '''
                                     The result of logical AND 
                                     of accumulator and 4-bit contents 
                                     of RAM currently addressed by B register 
                                     replaces contents of accumulator.
                                     ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-A&M"),
                             
         "OR":    ("Logical OR", 1,  '''
                                     The result of logic OR 
                                     of accumulator and 4-bit contents 
                                     of RAM currently addressed by B register 
                                     replaces contents of accumulator.
                                     ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-A|M"),
                             
         "EOR":    ("Logical Exclusive-OR", 1,  '''
                                     The result of logic Exclusive-OR 
                                     of accumulator and 4-bit contents 
                                     of RAM currently addressed by B register 
                                     replaces contents of accumulator.
                                     ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-A^M"),
                             
         "COMP":    ("Complement", 1,  '''
                                     Each bit of the accumulator is logically 
                                     complemented and placed in the accumulator.
                                     ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-~A"),
                             
         "XABL":    ("Exchange Accumulator and BL", 1,  '''
                                         The contents of accumulator and BL register 
                                         are exchanged.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<->BL"),
                             
         "LBUA":    ("Load BU with A", 1,  '''
                                         The contents of accumulator are 
                                         transferred to BU register.
                                         Also, the contents of currently
                                         addressed RAM are transferred to 
                                         accumulator. 
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "BU<-A\nA<-M"),
                             
         "LBMX":    ("Load BM with X", 1,  '''
                                         The contents of X register are 
                                         transferred to BM register.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "BM<-X"),
                             
         "XBMX":    ("Exchange BM and X", 1,  '''
                                         The contents of BM register and X 
                                         register are exchanged
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "X<->BM"),
                             
         "XAX":    ("Exchange Accumulator and X", 1,  '''
                                         The contents of accumulator and X 
                                         register are exchanged
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "X<->A"),
                             
         "LAX":    ("Load Accumulator from X Register", 1,  '''
                                         The 4-bit contents of the X register 
                                         are placed in the accumulator.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-X"),
                             
         "LXA":    ("Load X Register from Accumulator", 1,  '''
                                         The contents of the accumulator 
                                         are transferred to the X register.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "X<-A"),
                             
         "DIA":    ("Discrete Input Group A", 1,  '''
                                         Data at the inputs to discrete:
                                         Group A is transferred to the accumulator.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-DIA"),
                             
         "DIB":    ("Discrete Input Group B", 1,  '''
                                         Data at the inputs to discrete:
                                         Group B is transferred to the accumulator.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-DIB"),
                             
         "DOA":    ("Discrete Output", 1,  '''
                                         The contents of the accumulator 
                                         are transferred to the discrete output register.
                                         ''',
                                 '''
                                 N/A
                                 ''',
                                 "DOA<-A"),
                             
        "IOL":    ("Input/Output Long", 2,   '''
                                             This instruction occupies two ROM
                                             words and requires two cycles for
                                             execution. The first ROM word is
                                             I/O Enable signal.
                                             The second ROM word is then received by the I/O
                                             devices and decoded for address and command.
                                             The contents of the accumulator inverted
                                             are placed on the data lines for acceptance
                                             by the I/O. At the same time, input
                                             data received by the I/O device
                                             is transferred to the accumulator inverted.
                                             ''',
                                 '''
                                 N/A
                                 ''',
                                 "/A->Data Bus\nA<-/Data Bus\nI2->I/O Device"),
                             
        "T":    ("Transfer", 1,  '''
                                 An unconditional transfer to a ROM word
                                 on the current page takes place. The least
                                 significant 6-bits of P register P(6:1)
                                 are replaced by six bit immediate field
                                 I(6:1)
                                 ''',
                                 '''
                                 N/A
                                 ''',
                                 "P(6:1)<-I(6:1)"),
                             
        "TL":    ("Transfer Long", 2,  '''
                                 This instruction executes a transfer to any ROM 
                                 word on any page. It occupies two ROM words and 
                                 requires two cycles for execution.
                                 The first byte loads P(12:9) with field 
                                 I1(4:1) and then the second byte I2(8:1) is
                                 placed in P(8:1)
                                 ''',
                                 '''
                                 N/A
                                 ''',
                                 "P(12:9)<-I1(4:1)\nP(8:1)<-I2(8:1)"),
                             
        "TML":    ("Transfer and Mark Long", 2,  '''
                                 This instruction executes a transfer and 
                                 mark to any location on ROM page 
                                 4 through 15. It occupies two ROM words 
                                 and requires two cycle times for execution.
                                 ''',
                                 '''
                                 I1(2:1)!=00
                                 ''',
                                 "SB<-SA\nSA<-P\nP(12:9)<-I1(4:1)\nP(8:1)<-I2(8:1)"),
                             
        "TM":    ("Transfer and Mark Indirect", 2,  '''
                                 48 consecutive locations on ROM page 3 
                                 contains pointer data which identify 
                                 subroutine entry addresses.
                                 These subroutine entry addresses are 
                                 limited to pages 4 through 7.
                                 This TM instruction will save the 
                                 address of the next ROM word in 
                                 the SA register after loading 
                                 the original contents of SA into SB.
                                 A transfer then occurs to one of the subroutine 
                                 entry addresses. This instruction occupies 
                                 one ROM word but takes two cycles for 
                                 execution.
                                 ''',
                                 '''
                                 I(6:5)!=00
                                 ''',
                                 "SB<-SA\nSA<-P\nP(12:7)<-000011\nP(6:1)<-I1(8:1)\nP(12:9)<-0001\nP(8:1)<-I2(8:1)"),
                             
        "LDI":  ("Load Accumulator Immediate", 1, 
                                 '''
                                 The 4-bit contents, immediate field I[4:1],
                                 of the instruction are placed in accumulator.
                                 ''',
                                 '''
                                 Only the first occurrence of an LDI in a consecutive
                                 string of LDI's will be executed. The program will 
                                 ignore the remaining LDI's and execute next valid instruction.
                                 ''',
                                 "A<-|I(4:1)|"),
                                 
        "ADI":  ("Add Immediate and skip on carry-out", 1, 
                                 '''
                                 The result of binary addition of contents 
                                 of accumulator and 4-bit immediate 
                                 field of instruction word replaces the contents  
                                 of accumulator. The next ROM word will be 
                                 skipped (ignored) if a carry-out 
                                 is generated. This instruction does not 
                                 use or change the C flip-flop.
                                 The immediate field I(4:1) 
                                 of this instruction may not be equal to 
                                 binary 0000 or 1010 (See CYS and DC)
                                 ''',
                                 '''
                                 ''',
                                 "A<-A+|I(4:1)|\nSkip if carry-out=one\nI(4:1)!=0000\nI(4:1)!=1010"),
                                 
        "DC":  ("Decimal Correction", 1, 
                                 '''
                                 Binary 1010 is added to contents 
                                 of accumulator. Result is stored in accumulator.
                                 Instruction does not use or change 
                                 carry flip-flop or skip.
                                 ''',
                                 '''
                                 ''',
                                 "A<-A+|I(4:1)|\nSkip if carry-out=one\nI(4:1)!=0000\nI(4:1)!=1010"),
                                 
        "SKZ":  ("Skip on Accumulator Zero", 1, 
                                 '''
                                 The next ROM word will be ignored if 
                                 accumulator is 0.
                                 ''',
                                 '''
                                 ''',
                                 "skip if A=0000"),
                                 
        "SKF2":  ("Skip if FF2 Equals 1", 1, 
                                 '''
                                 The next ROM word will be ignored if 
                                 FF2 is 1.
                                 ''',
                                 '''
                                 ''',
                                 "skip if FF2=1"),
                                 
        "SKF1":  ("Skip if FF1 Equals 1", 1, 
                                 '''
                                 The next ROM word will be ignored if 
                                 FF1 is 1.
                                 ''',
                                 '''
                                 ''',
                                 "skip if FF1=1"),
                                 
        "SKC":  ("Skip on Carry flip-flop", 1, 
                                 '''
                                 The next ROM word will be ignored if 
                                 C flip-flop is 1.
                                 ''',
                                 '''
                                 ''',
                                 "skip if C=1"),
                                 
        "SKBI":  ("Skip if BL equals to Immediate.", 1, 
                                 '''
                                 The next ROM word will be ignored if 
                                 the the least significant four 
                                 bits of B register (BL) is equal 
                                 to the 4-bit immediate field 
                                 I(4:1) of instruction.
                                 ''',
                                 '''
                                 ''',
                                 "skip if BL=I(4:1)"),
                                 
        "RF1":  ("Reset FF1", 1, 
                                 '''
                                 Flip-flop 1 is  set to 0.
                                 ''',
                                 '''
                                 ''',
                                 "FF1<-0"),
                                 
        "SF1":  ("Set FF1", 1, 
                                 '''
                                 Flip-flop 1 is  set to 1.
                                 ''',
                                 '''
                                 ''',
                                 "FF1<-1"),
                                 
        "SF2":  ("Set FF2", 1, 
                                 '''
                                 Flip-flop 2 is  set to 1.
                                 ''',
                                 '''
                                 ''',
                                 "FF2<-1"),
                                 
        "SC":  ("Set Carry flip-flop", 1, 
                                 '''
                                 The C Flip-flop is  set to 1.
                                 ''',
                                 '''
                                 ''',
                                 "C<-1"),
                                 
        "RC":  ("Reset Carry flip-flop", 1, 
                                 '''
                                 The C Flip-flop is  set to 0.
                                 ''',
                                 '''
                                 ''',
                                 "C<-0"),
                                 
        "RF2":  ("Reset FF2", 1, 
                                 '''
                                 Flip-flop 2 is  set to 0.
                                 ''',
                                 '''
                                 ''',
                                 "FF2<-0"),
                                 
        "EXD":  ("Exchange Accumulator and Memory and decrement BL", 1, 
                                 '''
                                 Same as EX except RAM address in B register 
                                 is further modified by decrementing BL by 1.
                                 If the new contents of BL is 1111, the next 
                                 ROM word will be ignored
                                 ''',
                                 '''
                                 ''',
                                 "A<->M\nB(7:5)<-B(7:5)xor|I(3:1)|\nBL<-BL-1\nskip on BL=1111"),
                                 
        "EX":  ("Exchange Accumulator and Memory", 1, 
                                 '''
                                 Same as LD except the contents of accumulator 
                                 are also placed in currently addressed RAM location.
                                 ''',
                                 '''
                                 ''',
                                 "A<->M\nB(7:5)<-B(7:5)xor|I(3:1)|"),
                                 
                                         
        }
    
    
class RAM:
    LINELENGTH  = 8
    def __init__(self, length=256):
        self.mem = bytearray(length)
        for i in range(len(self.mem)):
            self.mem[i] = random.randint(0, 15)        

    def lby8(self):
        ret=list()
        for i in range(0,len(self.mem),8):  
            ret.append(self.mem[i:i+8])  
        return ret  
              
    def show(self, start=0, *, length=-1):  
        #print("size:", length) 
        if length == -1:
            length = len(self.mem)
        
    
        addr = start
        for x in self.mem[start:]:
            if not addr%self.LINELENGTH:
                print("\n{0:04X}\t".format(addr), end=' ')
            print("{0:02X}".format(x), end=' ')
            addr+=1
        print()
        
        
    
class ROM12(RAM):
    def __init__(self, fprom):
        self.mem = bytearray(fprom.read())

    def countinstoccur(self):
        cntinst={x: 0 for x in range(0,256)}

        CodHex = {} 
        for key, value in PPS4InstSet.HexCod.items(): 
            for i in value:
                if i in CodHex.keys(): 
                    CodHex[i].append(key)
                else: 
                    CodHex[i]=[key] 
  
        for inst in self.mem:
            cntinst[inst] += 1
            
        ret = {}
        #print(CodHex)
        for i in range(256):
            try:
                ret[CodHex[i][0]] = cntinst[i] + ret.get(CodHex[i][0], 0)
                if cntinst[i]==0:
                    print("==>",i,CodHex[i][0],"is never used")
            except:
                ret[i] = cntinst[i]
                #print("++>",i,"is not coded in codhex")
                
        
        
        return ret
            
        

def incr(r):
    r.incr()
    return r
         
class Pps4Cpu:
    rd = 0
    wr = 1
    
    iodev  = 1
    ramdev = 0
    def __init__(self, mode="trace", ROM=None):
        '''
        registers are lists of '0' and '1'
        the index 0 is bit 0, index 1 is bit 1 and so forth
        to convert a list to int one must do:
        int("".join(reversed(reg)), 2)
        and conversely:
        list("{0:08b}".format(romi)).reverse()
        
        This way, we have reg[0] which is actually bit 0
        default mode is trace. If set mode to "dasm", then simply disassemble code
        ROM is only used to determine indirect address of the TM instruction, and only in disassemnbly mode (offline)
        '''
        self.mode = mode
        self.ROM  = ROM
        self.A  = Register(4*['0'])  #Accumulator
        self.X  = Register(4*['0'])  #Accumulator
        self.BL = Register(4*['0'])
        self.BM = Register(4*['0'])
        self.BU = Register(4*['0'])
        self.C  = Register(['0'])
        self.FF1 = Register(['0'])
        self.FF2 = Register(['0'])
        self.P  = Register(12*['0'])
        self.AB = Register(12*['0'])
        self.SA = Register(12*['0'])
        self.SB = Register(12*['0'])
        
        self.DOA  = Register(4*['0'])  #Discrete output register
        self.DIA  = Register(4*['0'])  #Discrete input register group A
        self.DIB  = Register(4*['0'])  #Discrete input register group B

        #self.I1 = Register(8*['0'])
        self.I1 = None
        self.I2 = Register(8*['0'])
        self.lastI1 = None 
        self.nextIis2Cycles = False
        self.skipNext = False
        self.ramd   = None
        self.ramout = None
        self.wio    = None
        self.wramio = None
        
  
    def printcontext(self):
        print (" A:", self.A, "\tX:", self.X)
        print ("BL:", self.BL, "\tBM", self.BM, "\tBU", self.BU)
        print (" C:", self.C, "\tFF1", self.FF1, "\tFF2", self.FF2)
        print (" P:", "{0:03X}".format(self.P.toInt()))
        print ("AB:", self.AB)
        print ("SA:", "{0:03X}".format(self.SA.toInt()), "\tSB", "{0:03X}".format(self.SB.toInt()))
        print ("DIA:", self.DIA, "\tDIB", self.DIB, "\tDOA", self.DOA)
        print ('cur ram loaded', self.ramd)
            
    def htmlshortcontext(self):    
        ret =  "A: {0:01X}    X: {1:01X}".format(self.A.toInt(), self.X.toInt())
        ret+= "<br>"
        ret+= "B: {0:03X}".format((self.BL+self.BM+self.BU).toInt())
        ret+= "<br>"
        ret+=  "C: {0:01X}    FF1: {1:01X}    FF2: {2:01X}".format(self.C.toInt(), self.FF1.toInt(), self.FF2.toInt())

        return ret
    
    
    def is2CyclesInst(self, inst):
        '''
         2 cycles insts are:
        C0..CF : LB (load B indirect)               1100 xxxx
        00     : LBL (load B long)                  0000 0000
        D0..FF : TM (Transfer and mark indirect)    11x1 xxxx or 111x xxxx
        50..5F : TL (Transfer long)                 0101 xxxx
        01..03 : TML (Transfer and mark long)       0000 00xy (x=y=0 forbid)
        1C     : IOL                                0001 1100
        16+1+32+16+3+1=>69 instructions are 2 cycles
        '''
        if inst >= 0 and inst<= 3:
            return(True)
        if inst >= 0xC0 and inst<= 0xCF:
            return(True)
        if inst >= 0xD0 and inst<= 0xFF and self.mode != "dasm":
            return(True)
        if inst >= 0x50 and inst<= 0x5F:
            return(True)
        if inst == 0x1C:
            return(True)
        return False
        
    def cyclephi2(self, ramd):
        '''
        First part of the cpu cycle.
        CPU set addresses to the ROM byte it wants to read (P)
        return A, P, WIO
        A is the current content of accumulator, P the current programm counter, WIO the WIO signal
        '''
        self.ramd = Register("{0:04b}".format(ramd))
        
        #Now need to manage case IOL
        if self.I1 == Register(b"00011100") and not self.nextIis2Cycles:
            #print("etape derniere in cyclephi2", self.ramd)
            self.A = self.ramd[:]
            
        return self.AB.toInt(), self.wio
        
    def cyclephi4(self, romi):
        '''
        First part of the cpu cycle (phi4)
        
        CPU: - read and execute instruction Ii
             - set addresses to the next RAM byte it wants to read
             - return the disassembly text of what it has executed
             - says if next action is ram or io
        
        romi contains the instruction.
        ROM can be used if it is defined for TM instruction only
        it is to determine the indirect target address
        '''
        isThisaSetByt = False #default

        self.wio    = Pps4Cpu.rd #default
        self.wramio = Pps4Cpu.ramdev #default
        #print("handling", "{0:08b}".format(romi))
        if self.nextIis2Cycles:
            self.I2 = Register("{0:08b}".format(romi))
            #print("second inst", self.I2, "{0:08b}".format(romi))
            
        else:
            #one must check if it's an LDI, LB or LBL 
            #for these instructions, only the first in a string is executed
            self.lastI1 = self.I1
            self.I1 = Register("{0:08b}".format(romi))
            #print("first  inst", self.I1, "{0:08b}".format(romi))
            if self.is2CyclesInst(romi):
                if self.P[:6] == Register(b"111111") and self.mode == "dasm":
                    #this is a typical case of impossible instruction
                    #because we are at the frontier of a page for a bi-cycle instruction
                    #so we created the set nib instruction with isThisaSetByt
                    self.nextIis2Cycles = False
                    isThisaSetByt = True    
                    self.P.incr()
                else:
                    #we are in the first half of a 2-cycle inst
                    self.nextIis2Cycles = True
                    #Caution! There is the case of TM or LB
                    if self.I1[6:] == Register(b"11") and \
                       (self.I1.bit(4) or self.I1.bit(5)):  #TM
                        self.AB = self.I1[:6]+Register(b"000011")
                        #self.P  = incr(self.P[:6])+self.P[6:]
                        if self.mode != "dasm":
                            self.P  = incr(self.P[:6])+self.P[6:]
                            self.SB, self.SA = self.SA[:], self.P[:]
                            self.P  = self.I1[:6]+Register(b"000011")
                        else:
                            self.P.incr()
                    elif self.I1[4:] == Register(b"1100"):  #LB
                        if self.mode != "dasm":
                            self.SB = self.SA[:]
                            self.P  = incr(self.P[:6])+self.P[6:]
                            self.SA = self.P[:]                    
                            self.P = self.I1[:4] + Register(b"00001100")
                        else:
                            self.P.incr()                            
                    else:
                        #standard case of 2 cycles instructions
                        if self.mode != "dasm":
                            self.P = incr(self.P[:6])+self.P[6:]
                            self.AB = self.P[:]
                        else:
                            self.P.incr()                            
                    #print("self.P", self.P)
                    return (self.BL+self.BM+self.BU).toInt(), None, self.wramio 
            else:
                #this is a one cycle instruction
                self.nextIis2Cycles = False
            
        #print("self.P", self.P)
        ldis = self.cpuexe(isThisaSetByt)
        self.AB = self.P[:]
        
        #SAG handling
        if self.I1 == Register(b"00010011"):
            return (self.BL+Register(b"00000000")).toInt(), ldis, self.wramio
        return (self.BL+self.BM+self.BU).toInt(), ldis, self.wramio
        
    def cpuexe(self, isThisaSetByt=False):
        
        if self.nextIis2Cycles:
            ldis = self.P.toInt()-1, self.I1.toInt(), self.I2.toInt()
        else:
            ldis = self.P.toInt(), self.I1.toInt(), None
        #print("skipnext", self.skipNext)
        # if self.skipNext == False:
        #     myphrase = self.instdoc()
        # else:
        #     myphrase = "SKIP"
        #     self.P = incr(self.P[:6])+self.P[6:]
        #     self.skipNext = False
        self.skipNext = False  #just for info, does not take part in anything else
        if isThisaSetByt:
            myphrase = "SET NIB\t#{0:01X}".format(self.I1.toInt())
        else:
            myphrase, pipo = self.instdoc()
                
        
        self.nextIis2Cycles = False
        return ldis, myphrase
    
    def instdoc(self):
        '''
        '''
        '''
        LBL (00)
        ''' 
        if self.I1 == Register(b"00000000"):     
            #simulate
            ctxtxt=""
            if self.mode != "dasm":
                #The left clause will be evaluated first, and then the right one only if the first one is False.
                #This is why you can do stuff like:
                if self.lastI1 is not None and self.lastI1 == Register(b"00000000"):
                    #this is a string of LBL's only first counts others are nop
                    ctxtxt="\t"+"(NOP: series of LBL's)"
                else:
                    self.BU = Register(b"0000")
                    self.BM = ~self.I2[4:8]
                    self.BL = ~self.I2[0:4]

                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()
            #render phrase
            instcode="LBL"
            instphrase = instcode+"\t"+"{0:03X}".format((~self.I2).toInt())
            instphrase += ctxtxt
            return instphrase, None

        '''LABL (11)''' 
        if self.I1 == Register(b"00010001"):     
            #simulate
            if self.mode != "dasm":
                self.A = self.BL[:]
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="LABL"
            instphrase = instcode
            return instphrase, None

        '''LBUA (04)''' 
        if self.I1 == Register(b"00000100"):     
            #simulate
            if self.mode != "dasm":
                self.BU = self.A[:]
                self.A = self.ramd
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="LBUA"
            instphrase = instcode
            return instphrase, None

        '''LBMX (10)''' 
        if self.I1 == Register(b"00010000"):     
            #simulate
            if self.mode != "dasm":
                self.BM = self.X[:]
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="LBMX"
            instphrase = instcode
            return instphrase, None

        '''RF2 (25)''' 
        if self.I1 == Register(b"00100101"):     
            #simulate
            if self.mode != "dasm":
                self.FF2 = Register(b"0")
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="RF2"
            instphrase = instcode
            return instphrase, None

        '''SC (20)''' 
        if self.I1 == Register(b"00100000"):     
            #simulate
            if self.mode != "dasm":
                self.C = Register(b"1")
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="SC"
            instphrase = instcode
            return instphrase, None

        '''RC (20)''' 
        if self.I1 == Register(b"00100100"):     
            #simulate
            if self.mode != "dasm":
                self.C = Register(b"0")
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="RC"
            instphrase = instcode
            return instphrase, None

        '''SF2 (21)''' 
        if self.I1 == Register(b"00100001"):     
            #simulate
            if self.mode != "dasm":
                self.FF2 = Register(b"1")
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="SF2"
            instphrase = instcode
            return instphrase, None

        '''SF1 (22)''' 
        if self.I1 == Register(b"00100010"):     
            #simulate
            if self.mode != "dasm":
                self.FF1 = Register(b"1")
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="SF1"
            instphrase = instcode
            return instphrase, None

        '''RF1 (26)''' 
        if self.I1 == Register(b"00100110"):     
            #simulate
            if self.mode != "dasm":
                self.FF1 = Register(b"0")
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="RF1"
            instphrase = instcode
            return instphrase, None

        #CYS (6F)  
        if self.I1 == Register(b"01101111"):     
            #simulate
            if self.mode != "dasm":
                self.A, self.SA[:4], self.SA[4:8], self.SA[8:] = self.SA[:4], self.SA[4:8], self.SA[8:], self.A
            
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="CYS"
            instphrase = instcode
            return instphrase, None

        '''AND (0D) ''' 
        if self.I1 == Register(b"00001101"):     
            #simulate
            if self.mode != "dasm":
                self.A = self.A & self.ramd
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="AND"
            instphrase = instcode
            return instphrase, None

        '''COMP (0E) ''' 
        if self.I1 == Register(b"00001110"):     
            #simulate
            if self.mode != "dasm":
                self.A = ~self.A
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="COMP"
            instphrase = instcode
            return instphrase, None

        '''ADCSK (08)'''  
        if self.I1 == Register(b"00001000"):     
            #simulate
            ctxtxt=""
            if self.mode != "dasm":
                carry1, self.A = self.A.binAdd(self.C+Register(b"000"))
                carry2, self.A = self.A.binAdd(self.ramd)
                if carry1 == '0' and carry2 == '0':
                    self.C = Register('0')
                else:
                    self.C = Register('1')
                if carry1 == '1' and carry2 == '1':
                    print("dubious case in ADCSK, carry and carry2 are set")
                
                
                if self.C == Register('1'):
                    #skip next ROM word
                    self.P = incr(self.P[:6])+self.P[6:]
                    ctxtxt="\t(C=1 ==> skip)"
                else:
                    ctxtxt=""  
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()
            
                  
            #render phrase
            instcode="ADCSK"
            instphrase = instcode+ctxtxt
            return instphrase, None

        '''ADSK (09)'''  
        if self.I1 == Register(b"00001001"):     
            #simulate
            ctxtxt=""
            if self.mode != "dasm":
                carry, self.A = self.A.binAdd(self.ramd)
                self.C = Register(carry)                
                
                if carry == '1':
                    #skip next ROM word
                    self.P = incr(self.P[:6])+self.P[6:]
                    ctxtxt="\t(C=1 ==> skip)"
                else:
                    ctxtxt=""  
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()
                  
            #render phrase
            instcode="ADSK"
            instphrase = instcode+ctxtxt
            return instphrase, None

        '''ADC (0A)'''  
        if self.I1 == Register(b"00001010"):     
            #simulate
            ctxtxt=""
            if self.mode != "dasm":
                ctxtxt = "\t(C,A<=C({0:01X})+A({1:01X})+M({2:01X})".format(self.C.toInt(),
                                                                           self.A.toInt(),
                                                                           self.ramd.toInt())
                carry1, self.A = self.A.binAdd(self.C+Register(b"000"))
                carry2, self.A = self.A.binAdd(self.ramd)
                if carry1 == '0' and carry2 == '0':
                    self.C = Register('0')
                else:
                    self.C = Register('1')
                if carry1 == '1' and carry2 == '1':
                    print("dubious case in ADC, carry and carry2 are set")

                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()
            
            #render phrase
            instcode="ADC"
            instphrase = instcode+ctxtxt
            return instphrase, None

        '''AD (0B)'''  
        if self.I1 == Register(b"00001011"):     
            #simulate
            if self.mode != "dasm":
                carry, self.A = self.A.binAdd(self.ramd)
                self.C = Register(carry)
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()
            
            #render phrase
            instcode="AD"
            instphrase = instcode
            return instphrase, None

        '''EOR (0C)'''  
        if self.I1 == Register(b"00001100"):     
            #simulate
            if self.mode != "dasm":
                self.A = self.A ^ self.ramd
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="EOR"
            instphrase = instcode
            return instphrase, None

        #OR (0F)  
        if self.I1 == Register(b"00001111"):     
            #simulate
            if self.mode != "dasm":
                self.A = self.A | self.ramd
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="OR"
            instphrase = instcode
            return instphrase, None

        '''SKF2 (14)'''  
        if self.I1 == Register(b"00010100"):     
            #simulate
            if self.mode != "dasm":
                if not self.FF2.isZero():
                    #skip next instruction
                    #can't just increment P from here because
                    #we don't know nothing about the length of next instruction
                    #self.P = incr(self.P[:6])+self.P[6:]
                    #might be superfluous because the datasheet
                    #indicates "next ROM word"
                    #so we have to check (TODO)
                    self.skipNext = True
                    self.P = incr(self.P[:6])+self.P[6:]
                    #print("skipnext is True from incr", self.skipNext)
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="SKF2"
            instphrase = instcode
            return instphrase, None

        '''SKF1 (16)'''  
        if self.I1 == Register(b"00010110"):     
            #simulate
            if self.mode != "dasm":
                if not self.FF1.isZero():
                    #skip next instruction
                    #can't just increment P from here because
                    #we don't know nothing about the length of next instruction
                    #self.P = incr(self.P[:6])+self.P[6:]
                    #might be superfluous because the datasheet
                    #indicates "next ROM word"
                    #so we have to check (TODO)
                    self.skipNext = True
                    self.P = incr(self.P[:6])+self.P[6:]
                    #print("skipnext is True from incr", self.skipNext)
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="SKF1"
            instphrase = instcode
            return instphrase, None
        
        '''SKC (15)'''  
        if self.I1 == Register(b"00010101"):     
            #simulate
            if self.mode != "dasm":
                if not self.C.isZero():
                    #skip next instruction
                    #can't just increment P from here because
                    #we don't know nothing about the length of next instruction
                    #self.P = incr(self.P[:6])+self.P[6:]
                    #might be superfluous because the datasheet
                    #indicates "next ROM word"
                    #so we have to check (TODO)
                    self.skipNext = True
                    self.P = incr(self.P[:6])+self.P[6:]
                    #print("skipnext is True from incr", self.skipNext)
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="SKC"
            instphrase = instcode
            return instphrase, None
          
        '''SKZ (1E)'''  
        if self.I1 == Register(b"00011110"):     
            #simulate
            if self.mode != "dasm":
                if self.A.isZero():
                    #skip next instruction
                    #can't just increment P from here because
                    #we don't know nothing about the length of next instruction
                    self.P = incr(self.P[:6])+self.P[6:]
                    self.skipNext = True
                    #print("skipnext is True from incr", self.skipNext)
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="SKZ"
            instphrase = instcode
            return instphrase, None
          
        #DECB (1F)  
        if self.I1 == Register(b"00011111"):     
            #simulate
            ctxtxt = ""
            if self.mode != "dasm":
                self.BL.decr()
                if self.BL == Register(b"1111"):
                    #skip next instruction
                    #can't just increment P from here because
                    #we don't know nothing about the length of next instruction
                    ctxtxt = "(skip)"
                    self.P = incr(self.P[:6])+self.P[6:]
                    self.skipNext = True
                else:
                    ctxtxt = "(BL={0:1X})".format(self.BL.toInt())

                    #print("skipnext is True from incr", self.skipNext)
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="DECB"
            instphrase = instcode+"\t" + ctxtxt
            return instphrase, None
 
        '''SKBI (40..4F)'''  
        if self.I1[4:] == Register(b"0100"):     
            #simulate
            ctxtxt = ""
            if self.mode != "dasm":
                if self.BL == self.I1[:4]:
                    #skip next instruction
                    #can't just increment P from here because
                    #we don't know nothing about the length of next instruction
                    ctxtxt = "(skip)"
                    self.P = incr(self.P[:6])+self.P[6:]
                else:
                    ctxtxt = "(BL={0:1X})".format(self.BL.toInt())                    
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="SKBI\t{0:1X}".format(self.I1[:4].toInt())
            instphrase = instcode+"\t" + ctxtxt
            return instphrase, None
            
        #INCB (17)  
        if self.I1 == Register(b"00010111"):     
            #simulate
            ctxtxt = ""
            if self.mode != "dasm":
                self.BL.incr()
                if self.BL.isZero():
                    #skip next instruction
                    #can't just increment P from here because
                    #we don't know nothing about the length of next instruction
                    self.P = incr(self.P[:6])+self.P[6:]
                    self.skipNext = True
                    ctxtxt = "(skip)"
                else:
                    ctxtxt = "(BL={0:1X})".format(self.BL.toInt())
                    
                    #print("skipnext is True from incr", self.skipNext)
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="INCB"
            instphrase = instcode+"\t" + ctxtxt
            return instphrase, None
            
        #XS (06)  
        if self.I1 == Register(b"00000110"):     
            #simulate
            if self.mode != "dasm":
                self.SA, self.SB = self.SB[:], self.SA[:]
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="XS"
            instphrase = instcode
            return instphrase, None
            
        #XABL (19)  
        if self.I1 == Register(b"00011001"):     
            #simulate
            ctxtxt = ""
            if self.mode != "dasm":
                self.A, self.BL = self.BL[:], self.A[:]
                ctxtxt = "\t(A<=>BL, A<={0:01X}, {1:01X}=>BL)".format(self.A.toInt(), self.BL.toInt())
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="XABL"
            instphrase = instcode+"\t" + ctxtxt
            return instphrase, None
            
        #XBMX (18)  
        if self.I1 == Register(b"00011000"):     
            #simulate
            if self.mode != "dasm":
                self.X, self.BM = self.BM[:], self.X[:]
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="XBMX"
            instphrase = instcode
            return instphrase, None
            
        #XAX (1A)  
        if self.I1 == Register(b"00011010"):     
            #simulate
            if self.mode != "dasm":
                self.X, self.A = self.A[:], self.X[:]
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="XAX"
            instphrase = instcode
            return instphrase, None
            
        #LAX (12)  
        if self.I1 == Register(b"00010010"):     
            #simulate
            if self.mode != "dasm":
                self.A = self.X[:]
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="LAX"
            instphrase = instcode
            return instphrase, None
            
        #LXA (1B)  
        if self.I1 == Register(b"00011011"):     
            #simulate
            if self.mode != "dasm":
                self.X = self.A[:]
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="LXA"
            instphrase = instcode
            return instphrase, None
            
        #DOA (1D)  
        if self.I1 == Register(b"00011101"):     
            #simulate
            if self.mode != "dasm":
                self.DOA = self.A[:]
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="DOA"
            instphrase = instcode
            return instphrase, None
            
        #DIB (23)  
        if self.I1 == Register(b"00100011"):     
            #simulate
            if self.mode != "dasm":
                self.A = self.DIB[:]
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="DIB"
            instphrase = instcode
            return instphrase, None
            
        #DIA (27)  
        if self.I1 == Register(b"00100111"):     
            #simulate
            if self.mode != "dasm":
                self.A = self.DIA[:]
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="DIA"
            instphrase = instcode
            return instphrase, None
            
        #RTN (05)  
        if self.I1 == Register(b"00000101"):     
            #simulate
            if self.mode != "dasm":
                self.P = self.SA[:]
                self.SA, self.SB = self.SB[:], self.SA[:]
            else:
                self.P.incr()
                

            #render phrase
            instcode="RTN"
            instphrase = instcode
            return instphrase, None
            
        #RTNSK (07)  
        if self.I1 == Register(b"00000111"):     
            #simulate
            if self.mode != "dasm":
                self.P = self.SA[:]
                self.SA, self.SB = self.SB[:], self.SA[:]
                self.P = incr(self.P[:6])+self.P[6:]   #to be confirmed
            else:
                self.P.incr()
            
            #render phrase
            instcode="RTNSK"
            instphrase = instcode
            return instphrase, None
            
        #IOL (1C) is todo at the moment. 
        if self.I1 == Register(b"00011100"):     
            #simulate
            ctxtxt= "\t"+"{0:01X}".format(self.I2.toInt())
            if self.mode != "dasm":
                self.P = incr(self.P[:6])+self.P[6:]
                self.wramio = Pps4Cpu.iodev #default
                self.ramout = self.A 
                #A affectation is made in cyclephase2() when data is available from io device
                # print("===2=== this is the value received in A at IOL", self.ramd)
                # self.A = self.ramd[:]
                opt = "SOS" if self.I2.bit(0) else "SES"
                ctxtxt = "\t"+"{0:01X} (B=0x{2:03X} sent A={3:01X})".format(self.I2.toInt(), opt, (self.BL+self.BM+self.BU).toInt(), self.A.toInt())
            else:
                self.P.incr()
                   
            #render phrase
            instcode="IOL"
            instphrase = instcode+"\t" + ctxtxt
            return instphrase, None

        #EX (38..3F). 
        if self.I1[3:] == Register(b"00111"):     
            #simulate
            ctxtxt=""
            if self.mode != "dasm":
                #print("avant", self.BL, self.BM, self.BU)
                addrcible = self.BL + self.BM + self.BU
                ctxtxt   = "mem({0:03X})<={1:01X}, {2:01X}=>Acc".format(addrcible.toInt(),
                                                                          self.A.toInt(),
                                                                          self.ramd.toInt())
                self.A, self.ramout = self.ramd[:], self.A[:]
                self.wio = Pps4Cpu.wr #default
    
                
                self.BM[:3] = self.BM[:3] ^ ~self.I1[:3]

                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #render phrase
            instcode="EX"
            instphrase = instcode+"\t"+"{0:01X}".format((~self.I1[:3]).toInt())
            instphrase += "\t"+ctxtxt
            return instphrase, None
            
            
        #EXD (28..2F). 
        if self.I1[3:] == Register(b"00101"):     
            #simulate
            ctxtxt=""
            if self.mode != "dasm":
                #print("avant", self.BL, self.BM, self.BU)
                addrcible = self.BL + self.BM + self.BU
                ctxtxt   = "mem({0:03X})<={1:01X}, {2:01X}=>Acc BL--".format(addrcible.toInt(),
                                                                          self.A.toInt(),
                                                                          self.ramd.toInt())
                self.A, self.ramout = self.ramd[:], self.A[:]
                self.wio = Pps4Cpu.wr #default
    
                
                self.BM[:3] = self.BM[:3] ^ ~self.I1[:3]
                self.BL.decr()
                if self.BL == Register(b"1111"):
                    #skip next instruction
                    #can't just increment P from here because
                    #we don't know nothing about the length of next instruction
                    self.P = incr(self.P[:6])+self.P[6:]
                    self.skipNext = True

                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()
                
            #print("apres", self.BL, self.BM, self.BU)

            
            #render phrase
            instcode="EXD"
            instphrase = instcode+"\t"+"{0:01X}".format((~self.I1[:3]).toInt())
            instphrase += "\t"+ctxtxt
            return instphrase, None
            
        '''T Transfer is in range 80..BF'''
        if self.I1.bit(7) and not self.I1.bit(6):
            #simulate
            target_addr = self.I1[:6]+self.P[6:]
            ctxtxt="\t"+"{0:03X}".format( target_addr.toInt() )
            if self.mode != "dasm":
                self.P = target_addr
            else:
                #pass
                #print("Target address", "{0:03X}".format( self.P.toInt()), "{0:03X}".format( target_addr.toInt()))
                self.P.incr()
                
            
            #render phrase
            instcode="T"
            instphrase = instcode+ctxtxt
            return instphrase, target_addr.toInt()
        
        '''SAG (13)'''
        if self.I1 == Register(b"00010011"): 
            #simulate
            if self.mode != "dasm":
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()

            #raise Exception(f"The SAG instruction is not yet implemented")
            
            #render phrase
            instcode="SAG"
            instphrase = instcode
            return instphrase, None

        '''TL Transfer Long is in range 50..5F'''
        if self.I1[4:] == Register(b"0101"): 
            #simulate
            if self.mode != "dasm":
                self.P = self.I2[:]+self.I1[:4]
            else:
                self.P.incr()
            
            #render phrase
            instcode="TL"
            instphrase = instcode+"\t"+"{0:03X}".format( (self.I2[:]+self.I1[:4]).toInt() )
            return instphrase, (self.I2[:]+self.I1[:4]).toInt()

        #LD Load Accumulator from Memory is 30..37
        if self.I1[3:] == Register(b"00110"):
            #simulate
            ctxtxt=""
            if self.mode != "dasm":
                self.A    = self.ramd
                addrcur   = (self.BL+self.BM+self.BU)
                self.BM[:3] = self.BM[:3] ^ ~self.I1[:3]
                ctxtxt = "\tA<={0:01X} (from @{1:03X})".format(self.ramd.toInt(), addrcur.toInt())
                
                self.P     = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()
            
            #render phrase
            instcode="LD"
            instphrase = instcode+"\t"+"{0:01X}".format((~self.I1[:3]).toInt())
            instphrase += ctxtxt
            return instphrase, None
                
        '''
        TM Transfer and mark Indirect is D0..FF
        TM is special because you need to put an address on the address bus which
        will not be equal to the current P and then restore the old one to continue
        '''
        if self.I1[6:] == Register(b"11") and \
           (self.I1.bit(4) or self.I1.bit(5)):
            #simulate
            if self.mode != "dasm":
                target_address = self.I2+Register(b"0001")
                ctxtxt = "\t{0:03X} (via ({1:02X}))".format((self.I2+Register(b"0001")).toInt(), self.I1.toInt())
                #self.SB, self.SA = self.SA[:], self.P[:]
                #self.SA    = incr(self.P[:6])+self.P[6:]
                #self.SA    = self.P[:6]+self.P[6:]
                self.P[8:] = Register(b"0001")
                self.P[:8] = self.I2[:]
            else:
                ####Achtung, things to do here for dasm mode?
                ctxtxt = "\t({0:02X})".format(self.I1.toInt())
                if self.ROM is not None:
                    target_address = Register("{0:08b}".format(self.ROM[self.I1.toInt()]))+Register(b"0001")
                    ctxtxt += "\t(target addr={0:03X})".format(target_address.toInt())
                self.P.incr()
                
            #render phrase
            instcode="TM"
            instphrase = instcode+ctxtxt
            return instphrase, target_address.toInt()
        
        #TML Transfer and mark Long is 01, 02 or 03
        if self.I1 == Register(b"00000001") or \
           self.I1 == Register(b"00000010") or \
           self.I1 == Register(b"00000011"): 
            #simulate
            ctxtxt = "\t{0:03X}".format((self.I2+self.I1[:4]).toInt())
            if self.mode != "dasm":
                self.SB, self.SA = self.SA[:], incr(self.P[:6])+self.P[6:]
                #self.SA    = incr(self.P[:6])+self.P[6:]
                self.P[8:] = self.I1[:4]
                self.P[:8] = self.I2[:]
            else:
                self.P.incr()
            
            #render phrase
            instcode="TML"
            instphrase = instcode+ctxtxt
            return instphrase, (self.I2+self.I1[:4]).toInt()
        
        #LDI is in range 70..7F
        if self.I1[4:] == Register(b"0111"):
            #simulate
            ctxtxt=""
            if self.mode != "dasm":
                if self.lastI1 is not None and self.lastI1[4:] == Register(b"0111"):
                    #this is a string of LDI's only first counts others are nop
                    ctxtxt = "\t"+"(NOP: series of LDI's)"
                else:
                    self.A = self.I1[:4] ^ Register(b"1111")
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()
            
            #render phrase
            instcode="LDI"
            instcode = instcode+"\t"+"{0:01X}".format( (self.I1[:4] ^ Register(b"1111")).toInt() )
            instphrase = instcode+ctxtxt
            return instphrase, None
            
            
        '''
        ADI is in range 60..6F, except 65 (DC) and 6F (CYS)
        but 65 falls in the generic case (except no skip on carry)
        '''
        if self.I1[4:] == Register(b"0110") and self.I1[:4] != Register(b"1111"):
            #simulate
            ctxtxt=""
            if self.mode != "dasm":
                ctxtxt="\t(C,A<=A({0:01X})+#{1:01X})".format(self.A.toInt(), (~(self.I1[:4])).toInt())
                carry, self.A = self.A.binAdd(~(self.I1[:4]))
                self.C = Register(carry)
                if carry == '1' and self.I1[:4] != Register(b"0101"):
                    #skip next instruction
                    #can't just increment P from here because
                    #we don't know nothing about the length of next instruction
                    self.P = incr(self.P[:6])+self.P[6:]
                    self.skipNext = True
                    
                self.P = incr(self.P[:6])+self.P[6:]
            else:
                self.P.incr()
            
            #render phrase
            if self.I1[:4] == Register(b"0101"):
                #this is a DC
                instcode="DC"
                instphrase = instcode
                return instphrase, None
            else:
                instcode="ADI"
                instphrase = instcode+"\t"+"{0:1X}".format((~self.I1[:4]).toInt())
                instphrase+=ctxtxt
                if self.C == Register(b"1"):
                    instphrase+="\twill skip"
                return instphrase, None

        # self.P = incr(self.P[:6])+self.P[6:]
        # return ""

        '''
        LB is in range C0..CF
        (while TM Transfer and mark Indirect is D0..FF)
        LB is special because you need to put an address the address bus which
        will not be equal to the current P
        LB, like LBL is ignored in a string of it, except the first one
        '''
        if self.I1[4:] == Register(b"1100"):
            #simulate
            ctxtxt=""
            if self.mode != "dasm":
                if self.lastI1 is not None and self.lastI1[4:] == Register(b"1100"):
                    #this is a string of LB's only first counts others are nop
                    ctxtxt = "\t"+"(NOP: series of LB's)"
                else:
                    self.BU = Register(b"0000")
                    self.BM = ~(self.I2[4:])
                    self.BL = ~(self.I2[:4])
                    
                    self.P = self.SA[:]
                    self.SA, self.SB = self.SB[:], self.SA[:]
    
                #already done in phase 1 of the instruction
                #self.P = incr(self.P[:6])+self.P[6:]
                print("Debug: called LB=============================================")
            else:
                self.P.incr()
                
            #render phrase
            instcode="LB"
            instphrase = instcode+"\t"+"{0:02X}".format((~self.I2).toInt())
            instphrase += ctxtxt
            return instphrase, None


        if self.mode != "dasm":
            self.P = incr(self.P[:6])+self.P[6:]
        else:
            self.P.incr()
        raise Exception(f"should not get there")
        return "", None
    
    