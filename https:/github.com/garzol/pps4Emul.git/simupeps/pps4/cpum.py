'''
Created on 26 nov. 2022

@author: garzol
'''
import random


class PPS4InstSet():
    '''
    Doc is integrally copied from the original datasheet
    
    dictionary such as:
    keycode:("instruction name", #cycle, "Description", "exceptions", "equation")
    ''' 
    HexCod = {
        "LBL":  [0x00],
        "TML":  [0x01, 0x02, 0x03],
        "RTN":  [0x05],
        "XS":   [0x06],
        "RTNSK":[0x07],
        "ADCSK":[0x08],
        "ADC":  [0x0A],
        "AD":   [0x0B],
        "AND":  [0x0D],
        "COMP": [0x0E],
        "OR":   [0x0F],
        "LBMX": [0x10],
        "LABL": [0x11],
        "LAX":  [0x12],
        "SKF2": [0x14],
        "SKC":  [0x15],
        "INCB": [0x17],
        "XBMX": [0x18],
        "XABL": [0x19],
        "XAX":  [0x1A],
        "LXA":  [0x1B],
        "IOL":  [0x1C],
        "SKZ":  [0x1E],
        "DECB": [0x1F],
        "SC":   [0x20],
        "SF2":  [0x21],
        "SF1":  [0x22],
        "RF2":  [0x25],
        "RF1":  [0x26],
        "EXD":  [x for x in range(0x28,0x30)],
        "LD":   [x for x in range(0x30,0x37)],
        "EX ":  [x for x in range(0x38,0x40)],
        "SKBI": [x for x in range(0x40,0x50)],
        "TL":   [x for x in range(0x50,0x60)],
        "ADI":  [x for x in range(0x60,0x65)]+[x for x in range(0x66,0x6F)],
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
                                 "SB<-SA\nSA<-P\nI2->I/O Device"),
                             
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
                                     The result of logical OR 
                                     of accumulator and 4-bit contents 
                                     of RAM currently addressed by B register 
                                     replaces contents of accumulator.
                                     ''',
                                 '''
                                 N/A
                                 ''',
                                 "A<-A|M"),
                             
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
                                 "P(6:1)<-I(6:1"),
                             
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
                                 "P(12:9)<-I1(4:1\nP(8:1)<-I2(8:1"),
                             
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
                                 
        "SKZ":  ("Skip on Accumulator Zero", 1, 
                                 '''
                                 The next ROM word will be ignored if 
                                 accumulator is 0.
                                 ''',
                                 "skip if A=0000"),
                                 
        "SKF2":  ("Skip if FF2 Equals 1", 1, 
                                 '''
                                 The next ROM word will be ignored if 
                                 FF2 is 1.
                                 ''',
                                 "skip if FF2=1"),
                                 
        "SKC":  ("Skip on Carry flip-flop", 1, 
                                 '''
                                 The next ROM word will be ignored if 
                                 C flip-flop is 1.
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
                                 "skip if BL=I(4:1)"),
                                 
        "RF1":  ("Reset FF1", 1, 
                                 '''
                                 Flip-flop 1 is  set to 0.
                                 ''',
                                 "FF1<-0"),
                                 
        "SF1":  ("Set FF1", 1, 
                                 '''
                                 Flip-flop 1 is  set to 1.
                                 ''',
                                 "FF1<-1"),
                                 
        "SF2":  ("Set FF2", 1, 
                                 '''
                                 Flip-flop 2 is  set to 1.
                                 ''',
                                 "FF2<-1"),
                                 
        "SC":  ("Set Carry flip-flop", 1, 
                                 '''
                                 The C Flip-flop is  set to 1.
                                 ''',
                                 "C<-1"),
                                 
        "RF2":  ("Reset FF2", 1, 
                                 '''
                                 Flip-flop 2 is  set to 0.
                                 ''',
                                 "FF2<-0"),
                                 
        "EXD":  ("Exchange Accumulator and Memory and decrement BL", 1, 
                                 '''
                                 Same as EX except RAM address in B register 
                                 is further modified by decrementing BL by 1.
                                 If the new contents of BL is 1111, the next 
                                 ROM word will be ignored
                                 ''',
                                 "A<->M\nB(7:5)<-B(7:5)xor|I(3:1)|\nBL<-BL-1\nskip on BL=1111"),
                                 
        "EX":  ("Exchange Accumulator and Memory", 1, 
                                 '''
                                 Same as LD except the contents of accumulator 
                                 are also placed in currently addressed RAM location.
                                 ''',
                                 "A<->M\nB(7:5)<-B(7:5)xor|I(3:1)|"),
                                 
                                         
        }
    
    
class RAM:
    LINELENGTH  = 8
    def __init__(self, length=256):
        self.mem = bytearray(length)
        for i in range(len(self.mem)):
            self.mem[i] = random.randint(0, 15)        
            
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
            
        
class Register(list): 
    addLaw = {
        ('0','0','0'): ('0','0'),
        ('0','0','1'): ('0','1'),
        ('0','1','0'): ('0','1'),
        ('0','1','1'): ('1','0'),
        ('1','0','0'): ('0','1'),
        ('1','0','1'): ('1','0'),
        ('1','1','0'): ('1','0'),
        ('1','1','1'): ('1','1'),
        }  
    
    def __init__(self, param=4):
        #
        #super(Register, self).__init__()
        #print("param is", param, type(param))
        if isinstance(param, bytes):
            self.bits = ['0' if i==48 else '1' for i in reversed(list(param))]      
        elif isinstance(param, int):
            self.bits = param*['0']
        elif isinstance(param, list):
            self.bits = list()
            for x in param:
                if x == '1':
                    self.bits.append('1')
                else:
                    self.bits.append('0')
        elif isinstance(param, str):
            self.bits = list()
            for x in reversed(param):
                if x == '1':
                    self.bits.append('1')
                else:
                    self.bits.append('0')
        elif param == '0' or param == '1':
            self.bits = [param]
        else:
            #self.bits = None
            raise Exception(f"Can't initialize this way (param, type param : {1} {0})".format(type(param), param))
            
                    
    def __getitem__(self, key):
        # if not type(key) is int:
        #     raise TypeError("Only integers are allowed in indices")
        #
        # if key>=len(self.bits) or key<0:
        #     raise IndexError("Index out of range")
        #print("__getitem__", key)           
        return Register(self.bits[key])

    def __setitem__(self, slp, data):
        
        self.bits[slp] = data
        #print("setitem:", self.bits)
        return Register(self.bits[slp])

    def __invert__(self):
        return Register(['1' if x == '0' else '0' for x in self.bits])
            
            
                    
    def __mul__(self, other):
        """Handle p * 5"""
        if isinstance(other, int):
            return Register(other*self.bits)
        
        raise TypeError(f'Cannot multiply a Register with {type(other)}')

    """Handle 5 * p"""
    __rmul__ = __mul__  
    
    def __and__(self, other):
        if not isinstance(other, Register):
            raise TypeError(f'Cannot anding a Register with {type(other)}')
        if len(self.bits) != len(other.bits):
            raise IndexError(f'Cannot anding Registers of different lengths')
        op = zip(self.bits, other.bits)

        ret=['1' if x[0]=='1' and x[1]=='1' else '0' for x in op]
        return Register(ret)
             
    def __or__(self, other):
        if not isinstance(other, Register):
            raise TypeError(f'Cannot oring a Register with {type(other)}')
        if len(self.bits) != len(other.bits):
            raise IndexError(f'Cannot oring Registers of different lengths')
        op = zip(self.bits, other.bits)

        ret=['1' if x[0]=='1' or x[1]=='1' else '0' for x in op]
        return Register(ret)
             
    def __xor__(self, other):
        if not isinstance(other, Register):
            raise TypeError(f'Cannot xoring a Register with {type(other)}')
        if len(self.bits) != len(other.bits):
            raise IndexError(f'Cannot xoring Registers of different lengths')
        op = zip(self.bits, other.bits)

        ret=['1' if x[0]!=x[1] else '0' for x in op]
        return Register(ret)
             
    def __str__(self):
        return "".join(reversed(self.bits))
 
    def __repr__(self):
        return "".join(reversed(self.bits))
 
    def __iter__(self):
        #print("__iter__")
        for x in self.bits:
            yield x

    def __add__(self, other):
        total_bits = self.bits + other.bits
        return Register(total_bits)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __eq__(self, other):
        if other is None:
            return False
        if len(self.bits) != len(other.bits):
            return False
        op = zip(self.bits, other.bits)

        for x in op:
            if x[0]!=x[1]: return False
        return True
    
    def __ne__(self, other):      
        return not self.__eq__(other)
        
        
        
                
    def isZero(self):
        for b in self.bits:
            if b != '0':
                return False
        return True    
    
    def bit(self, n):
        if n>=len(self.bits) or  n<0:
            raise IndexError(f'bit index is out of range of its Register')
        
        return 1 if self.bits[n]=='1' else 0
    
    def incr(self):
        '''
        ['0','1','0','1'] becomes ['1','1','0','1'] and returns '0'
        ['1','1','0','1'] becomes ['0','0','1','1'] and returns '0'
        ['1','1','1','1'] becomes ['0','0','0','0'] and returns '1'
        '''
        if not self.bits:
            raise Exception("Can't increment void register")
        if self.bits[0] == '0':
            self.bits[0] = '1'
            return '0'
        
        carry = '1'
        for  i in range(len(self.bits)):
            if carry == '0': break
            if self.bits[i] == '0': 
                self.bits[i] = '1'
                carry  = '0'
            else:
                self.bits[i] = '0'
                carry  = '1'
        return carry      
            
    def decr(self):
        '''
        Ex:
        b1111 becomes b1110, c=0
        b1110 becomes b1101, c=0
        ...
        b0000 becomes b1111, c=1
        '''
        if not self.bits:
            raise Exception("Can't decrement void register")
        
        carry = '1'
        for  i in range(len(self.bits)):
            if self.bits[i] == '1': 
                self.bits[i] = '0'
                carry = '0'
                break            
            else: 
                self.bits[i] = '1'
        return carry      
            
    def toInt(self):
        return int("".join(reversed(self.bits)), 2)

    def binAdd(self, other):
        if not isinstance(other, Register):
            raise TypeError(f'Cannot binary add a Register with {type(other)}')
        if len(self.bits) != len(other.bits):
            raise IndexError(f'Cannot binary add Registers of different lengths')
        op = zip(self.bits, other.bits)

        carry = '0'
        ret = list()
        for sb, ob in op:
            carry, x = Register.addLaw[carry, sb, ob]
            ret.append(x)
        return carry, Register(ret)

def incr(r):
    r.incr()
    return r
         
class Pps4Cpu:
    rd = 0
    wr = 1
    def __init__(self):
        '''
        registers are lists of '0' and '1'
        the index 0 is bit 0, index 1 is bit 1 and so forth
        to convert a list to int one must do:
        int("".join(reversed(reg)), 2)
        and conversely:
        list("{0:08b}".format(romi)).reverse()
        
        This way, we have reg[0] which is actually bit 0
        '''
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
        self.I1 = Register(8*['0'])
        self.I2 = Register(8*['0'])
        self.lastI1 = None 
        self.nextIis2Cycles = False
        self.skipNext = False
        self.ramd   = None
        self.ramout = None
        self.wio    = None
        
  
            
            
             
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
        if inst >= 0xC0 and inst<= 0xFF:
            return(True)
        if inst >= 0x50 and inst<= 0x5F:
            return(True)
        if inst == 0x1C:
            return(True)
        return False
        
    def cyclephi12(self, ramd):
        '''
        First part of the cpu cycle.
        CPU set addresses to the ROM byte it wants to read (P)
        return A, P, WIO
        A is the current content of accumulator, P the current programm counter, WIO the WIO signal
        '''
        self.ramd = Register("{0:04b}".format(ramd))
        if self.ramout is not None:
            ramout = self.ramout.toInt()
        else:
            ramout = None
        
        return ramout, self.AB.toInt(), self.wio
        
    def cyclephi34(self, romi):
        '''
        Second part of the cpu cycle.
        CPU set addresses to the RAM byte it wants to read
        
        romi contains the instruction.
        '''
        self.wio = Pps4Cpu.rd #default
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
                #we are in the first half of a 2-cycle inst
                self.nextIis2Cycles = True
                #Caution! There is the case of TM or LB
                if self.I1[6:] == Register(b"11") and \
                   (self.I1.bit(4) or self.I1.bit(5)):  #TM
                    self.AB = self.I1[:6]+Register(b"000011")
                    self.P  = incr(self.P[:6])+self.P[6:]
                elif self.I1[4:] == Register(b"1100"):  #LB
                    self.SB = self.SA[:]
                    self.SA = self.P[:]                    
                    self.P = self.I1[:4] + Register(b"00001100")
                else:
                    #standard case of 2 cycles instructions
                    self.P = self.AB = incr(self.P[:6])+self.P[6:]
                #print("self.P", self.P)
                return (self.BL+self.BM+self.BU).toInt(), None 
            else:
                self.nextIis2Cycles = False
            
        #print("self.P", self.P)
        ldis = self.cpuexe()
        self.AB = self.P
        return (self.BL+self.BM+self.BU).toInt(), ldis
        
    def cpuexe(self):
        
        if self.nextIis2Cycles:
            ldis = "{0:04X}\t{1:02X} {2:02X}".format(self.P.toInt()-1, self.I1.toInt(), self.I2.toInt())
        else:
            ldis = "{0:04X}\t{1:02X}".format(self.P.toInt(), self.I1.toInt())
        #print("skipnext", self.skipNext)
        if self.skipNext == False:
            myphrase = self.instdoc()
        else:
            myphrase = "SKIP"
            self.P = incr(self.P[:6])+self.P[6:]
            self.skipNext = False
        
        self.nextIis2Cycles = False
        return ldis+"\t"+myphrase
    
    def instdoc(self):
        '''
        '''
        '''
        LBL (00)
        ''' 
        if self.I1 == Register(b"00000000"):     
            #simulate
            if self.lastI1 == Register(b"00000000"):
                #this is a string of LBL's only first counts others are nop
                pass
            else:
                self.BU = Register(b"0000")
                self.BM = ~self.I2[4:8]
                self.BL = ~self.I2[0:4]
            self.P = incr(self.P[:6])+self.P[6:]
            
            #render phrase
            if self.lastI1 == Register(b"00000000"):
                #this is a string of LDI's only first counts others are nop
                instcode="NOP"
                instphrase = instcode+"\t"+"(series of LBL's"
                return instphrase
            else:
                instcode="LBL"
                instphrase = instcode+"\t"+"{0:04X}".format((~self.I2).toInt())
                return instphrase

        '''LABL (11)''' 
        if self.I1 == Register(b"00010001"):     
            #simulate
            self.A = self.BL[:]
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="LABL"
            instphrase = instcode
            return instphrase

        '''LBMX (10)''' 
        if self.I1 == Register(b"00010000"):     
            #simulate
            self.BM = self.X[:]
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="LBMX"
            instphrase = instcode
            return instphrase

        '''RF2 (25)''' 
        if self.I1 == Register(b"00100101"):     
            #simulate
            self.FF2 = Register(b"0")
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="RF2"
            instphrase = instcode
            return instphrase

        '''SC (20)''' 
        if self.I1 == Register(b"00100000"):     
            #simulate
            self.C = Register(b"1")
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="SC"
            instphrase = instcode
            return instphrase

        '''SF2 (21)''' 
        if self.I1 == Register(b"00100001"):     
            #simulate
            self.FF2 = Register(b"1")
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="SF2"
            instphrase = instcode
            return instphrase

        '''SF1 (22)''' 
        if self.I1 == Register(b"00100010"):     
            #simulate
            self.FF1 = Register(b"1")
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="SF1"
            instphrase = instcode
            return instphrase

        '''RF1 (26)''' 
        if self.I1 == Register(b"00100110"):     
            #simulate
            self.FF1 = Register(b"0")
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="RF1"
            instphrase = instcode
            return instphrase

        #CYS (6F)  
        if self.I1 == Register(b"01101111"):     
            #simulate
            self.A, self.SA[:4], self.SA[4:8], self.SA[8:] = self.SA[:4], self.SA[4:8], self.SA[8:], self.A
            
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="CYS"
            instphrase = instcode
            return instphrase

        '''AND (0D) ''' 
        if self.I1 == Register(b"00001101"):     
            #simulate
            self.A = self.A & self.ramd
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="AND"
            instphrase = instcode
            return instphrase

        '''COMP (0E) ''' 
        if self.I1 == Register(b"00001110"):     
            #simulate
            self.A = ~self.A
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="COMP"
            instphrase = instcode
            return instphrase

        '''ADCSK (08)'''  
        if self.I1 == Register(b"00001000"):     
            #simulate
            carry, self.A = self.A.binAdd(self.ramd)
            self.C = Register(carry)
            carry, self.A = self.A.binAdd(self.C+Register(b"000"))
            self.C = Register(carry)
            self.P = incr(self.P[:6])+self.P[6:]
            if carry == '1':
                #skip next ROM word
                self.P = incr(self.P[:6])+self.P[6:]
                skptxt="\t(C=1 ==> skip)"
            else:
                skptxt=""  
                  
            #render phrase
            instcode="ADCSK"
            instphrase = instcode+skptxt
            return instphrase

        '''ADC (0A)'''  
        if self.I1 == Register(b"00001010"):     
            #simulate
            carry, self.A = self.A.binAdd(self.ramd)
            self.C = Register(carry)
            carry, self.A = self.A.binAdd(self.C+Register(b"000"))
            self.C = Register(carry)
            self.P = incr(self.P[:6])+self.P[6:]
            
            #render phrase
            instcode="ADC"
            instphrase = instcode
            return instphrase

        '''AD (0B)'''  
        if self.I1 == Register(b"00001011"):     
            #simulate
            carry, self.A = self.A.binAdd(self.ramd)
            self.C = Register(carry)
            self.P = incr(self.P[:6])+self.P[6:]
            
            #render phrase
            instcode="AD"
            instphrase = instcode
            return instphrase

        #OR (0F)  
        if self.I1 == Register(b"00001111"):     
            #simulate
            self.A = self.A | self.ramd
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="OR"
            instphrase = instcode
            return instphrase

        '''SKF2 (14)'''  
        if self.I1 == Register(b"00010100"):     
            #simulate
            if not self.FF2.isZero():
                #skip next instruction
                #can't just increment P from here because
                #we don't know nothing about the length of next instruction
                #self.P = incr(self.P[:6])+self.P[6:]
                #might be superfluous because the datasheet
                #indicates "next ROM word"
                #so we have to check (TODO)
                self.skipNext = True
                #print("skipnext is True from incr", self.skipNext)
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="SKF2"
            instphrase = instcode
            return instphrase
        
        '''SKC (15)'''  
        if self.I1 == Register(b"00010101"):     
            #simulate
            if not self.C.isZero():
                #skip next instruction
                #can't just increment P from here because
                #we don't know nothing about the length of next instruction
                #self.P = incr(self.P[:6])+self.P[6:]
                #might be superfluous because the datasheet
                #indicates "next ROM word"
                #so we have to check (TODO)
                self.skipNext = True
                #print("skipnext is True from incr", self.skipNext)
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="SKC"
            instphrase = instcode
            return instphrase
          
        '''SKZ (1E)'''  
        if self.I1 == Register(b"00011110"):     
            #simulate
            if self.A.isZero():
                #skip next instruction
                #can't just increment P from here because
                #we don't know nothing about the length of next instruction
                #self.P = incr(self.P[:6])+self.P[6:]
                self.skipNext = True
                #print("skipnext is True from incr", self.skipNext)
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="SKZ"
            instphrase = instcode
            return instphrase
          
        #DECB (1F)  
        if self.I1 == Register(b"00011111"):     
            #simulate
            self.BL.decr()
            if self.BL == Register(b"1111"):
                #skip next instruction
                #can't just increment P from here because
                #we don't know nothing about the length of next instruction
                #self.P = incr(self.P[:6])+self.P[6:]
                self.skipNext = True
                #print("skipnext is True from incr", self.skipNext)
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="DECB"
            if self.BL == Register(b"1111"):
                op = "(skip)"
            else:
                op = "(BL={0:1X})".format(self.BL.toInt())
            instphrase = instcode+"\t" + op
            return instphrase
 
        '''SKBI (40..4F)'''  
        if self.I1[4:] == Register(b"0100"):     
            #simulate
            if self.BL == self.I1[:4]:
                #skip next instruction
                #can't just increment P from here because
                #we don't know nothing about the length of next instruction
                self.P = incr(self.P[:6])+self.P[6:]
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="SKBI\t{0:1X}".format(self.I1[:4].toInt())
            if self.BL == self.I1[:4]:
                op = "(skip)"
            else:
                op = "(BL={0:1X})".format(self.BL.toInt())
            instphrase = instcode+"\t" + op
            return instphrase
            
        #INCB (17)  
        if self.I1 == Register(b"00010111"):     
            #simulate
            self.BL.incr()
            if self.BL.isZero():
                #skip next instruction
                #can't just increment P from here because
                #we don't know nothing about the length of next instruction
                #self.P = incr(self.P[:6])+self.P[6:]
                self.skipNext = True
                #print("skipnext is True from incr", self.skipNext)
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="INCB"
            if self.BL.isZero():
                op = "(skip)"
            else:
                op = "(BL={0:1X})".format(self.BL.toInt())
            instphrase = instcode+"\t" + op
            return instphrase
            
        #XS (06)  
        if self.I1 == Register(b"00000110"):     
            #simulate
            self.SA, self.SB = self.SB, self.SA
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="XS"
            instphrase = instcode
            return instphrase
            
        #XABL (19)  
        if self.I1 == Register(b"00011001"):     
            #simulate
            self.A, self.BL = self.BL, self.A
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="XABL"
            instphrase = instcode
            return instphrase
            
        #XBMX (18)  
        if self.I1 == Register(b"00011000"):     
            #simulate
            self.X, self.BM = self.BM, self.X
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="XBMX"
            instphrase = instcode
            return instphrase
            
        #XAX (1A)  
        if self.I1 == Register(b"00011010"):     
            #simulate
            self.X, self.A = self.A, self.X
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="XAX"
            instphrase = instcode
            return instphrase
            
        #LAX (12)  
        if self.I1 == Register(b"00010010"):     
            #simulate
            self.A = self.X[:]
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="LAX"
            instphrase = instcode
            return instphrase
            
        #LXA (1B)  
        if self.I1 == Register(b"00011011"):     
            #simulate
            self.X = self.A[:]
            self.P = incr(self.P[:6])+self.P[6:]

            #render phrase
            instcode="LXA"
            instphrase = instcode
            return instphrase
            
        #RTN (05)  
        if self.I1 == Register(b"00000101"):     
            #simulate
            self.P = self.SA[:]
            self.SA, self.SB = self.SB, self.SA

            #render phrase
            instcode="RTN"
            instphrase = instcode
            return instphrase
            
        #RTNSK (07)  
        if self.I1 == Register(b"00000111"):     
            #simulate
            self.P = self.SA[:]
            self.SA, self.SB = self.SB, self.SA
            self.P = incr(self.P[:6])+self.P[6:]   #to be confirmed

            #render phrase
            instcode="RTNSK"
            instphrase = instcode
            return instphrase
            
        #IOL (1C) is todo at the moment. 
        if self.I1 == Register(b"00011100"):     
            #simulate
            self.P = incr(self.P[:6])+self.P[6:]
               
            #render phrase
            instcode="IOL"
            opt = "SOS" if self.I2.bit(0) else "SES"
            instphrase = instcode+"\t"+"{0:01X} ({1} @{2:04X})".format(self.I2.toInt(), opt, (self.BL+self.BM+self.BU).toInt())
            return instphrase

        #EX (38..3F). 
        if self.I1[3:] == Register(b"00111"):     
            #simulate
            #print("avant", self.BL, self.BM, self.BU)
            self.A, self.ramout = self.ramd, self.A
            self.wio = Pps4Cpu.wr #default

            self.P = incr(self.P[:6])+self.P[6:]
            
            self.BM[:3] = self.BM[:3] ^ ~self.I1[:3]

            #render phrase
            instcode="EX"
            instphrase = instcode+"\t"+"{0:01X}".format((~self.I1[:3]).toInt())
            return instphrase
            
            
        #EXD (28..2F). 
        if self.I1[3:] == Register(b"00101"):     
            #simulate
            #print("avant", self.BL, self.BM, self.BU)
            self.A, self.ramout = self.ramd, self.A
            self.wio = Pps4Cpu.wr #default

            self.P = incr(self.P[:6])+self.P[6:]
            
            self.BM[:3] = self.BM[:3] ^ ~self.I1[:3]
            self.BL.decr()
            if self.BL == Register(b"1111"):
                #skip next instruction
                #can't just increment P from here because
                #we don't know nothing about the length of next instruction
                #self.P = incr(self.P[:6])+self.P[6:]
                self.skipNext = True
                
            #print("apres", self.BL, self.BM, self.BU)

            
            #render phrase
            instcode="EXD"
            instphrase = instcode+"\t"+"{0:01X}".format((~self.I1[:3]).toInt())
            return instphrase
            
        '''T Transfer is in range 80..BF'''
        if self.I1.bit(7) and not self.I1.bit(6):
            #simulate
            self.P = self.I1[:6]+self.P[6:]
            
            #render phrase
            instcode="T"
            instphrase = instcode+"\t"+"{0:04X}".format(self.P.toInt())
            return instphrase
        
        #Transfer Long is in range 50..5F
        if self.I1[4:] == Register(b"0101"): 
            #simulate
            self.P = self.I2[:8]+self.I1[:4]
            
            #render phrase
            instcode="TL"
            instphrase = instcode+"\t"+"{0:04X}".format(self.P.toInt())
            return instphrase

        #LD Load Accumulator from Memory is 30..37
        if self.I1[3:] == Register(b"00110"):
            #simulate
            self.A    = self.ramd
            self.BM[:3] = self.BM[:3] ^ ~self.I1[:3]

            self.P     = incr(self.P[:6])+self.P[6:]
            
            #render phrase
            instcode="LD"
            instphrase = instcode+"\t"+"{0:01X}".format((~self.I1[:3]).toInt())
            return instphrase
                
        '''
        TM Transfer and mark Indirect is D0..FF
        TM is special because you need to put an address the address bus which
        will not be equal to the current P
        '''
        if self.I1[6:] == Register(b"11") and \
           (self.I1.bit(4) or self.I1.bit(5)):
            #simulate
            self.SB, self.SA = self.SA, self.P[:]
            #self.SA    = incr(self.P[:6])+self.P[6:]
            #self.SA    = self.P[:6]+self.P[6:]
            self.P[8:] = Register(b"0001")
            self.P[:8] = self.I2
            #render phrase
            instcode="TM"
            instphrase = instcode+"\t"+"{0:04X}".format(self.P.toInt())
            return instphrase
        
        #TML Transfer and mark Long is 01, 02 or 03
        if self.I1 == Register(b"00000001") or \
           self.I1 == Register(b"00000010") or \
           self.I1 == Register(b"00000011"): 
            #simulate
            self.SB, self.SA = self.SA, incr(self.P[:6])+self.P[6:]
            #self.SA    = incr(self.P[:6])+self.P[6:]
            self.P[8:] = self.I1[:4]
            self.P[:8] = self.I2
            
            #render phrase
            instcode="TML"
            instphrase = instcode+"\t"+"{0:04X}".format(self.P.toInt())
            return instphrase
        
        #LDI is in range 70..7F
        if self.I1[4:] == Register(b"0111"):
            #simulate
            if self.lastI1[4:] == Register(b"0111"):
                #this is a string of LDI's only first counts others are nop
                pass
            else:
                self.A = self.I1[:4] ^ Register(b"1111")
            self.P = incr(self.P[:6])+self.P[6:]
            
            #render phrase
            if self.lastI1[4:] == Register(b"0111"):
                #this is a string of LDI's only first counts others are nop
                instcode="NOP"
                instphrase = instcode+"\t"+"(series of LDI's)"
                return instphrase
            else:
                instcode="LDI"
                instphrase = instcode+"\t"+"{0:01X}".format(self.A.toInt())
                return instphrase
            
            
        '''
        ADI is in range 60..6F, except 65 (DC) and 6F (CYS)
        but 65 falls in the generic case (except no skip on carry)
        '''
        if self.I1[4:] == Register(b"0110") and self.I1[:4] != Register(b"1111"):
            #simulate
            carry, self.A = self.A.binAdd(~(self.I1[:4]))
            self.P = incr(self.P[:6])+self.P[6:]
            if carry == '1' and self.I1[:4] != Register(b"0101"):
                #skip next instruction
                #can't just increment P from here because
                #we don't know nothing about the length of next instruction
                #self.P = incr(self.P[:6])+self.P[6:]
                self.skipNext = True
            
            #render phrase
            if self.I1[:4] == Register(b"0101"):
                #this is a DC
                instcode="DC"
                instphrase = instcode
                return instphrase
            else:
                instcode="ADI"
                instphrase = instcode+"\t"+"{0:1X}".format((~self.I1[:4]).toInt())
                return instphrase

        self.P = incr(self.P[:6])+self.P[6:]
        return ""

        '''
        LB is in range C0..CF
        (while TM Transfer and mark Indirect is D0..FF)
        LB is special because you need to put an address the address bus which
        will not be equal to the current P
        LB, like LBL is ignored in a string of it, except the first one
        '''
        if self.I1[4:] == Register(b"1100"):
            #simulate
            if self.lastI1[4:] == Register(b"1100"):
                #this is a string of LB's only first counts others are nop
                pass
            else:
                self.BU = Register(b"0000")
                self.BM = ~(self.I2[4:])
                self.BL = ~(self.I2[:4])
                
                self.P = self.SA[:]
                self.SA, self.SB = self.SB, self.SA

            self.P = incr(self.P[:6])+self.P[6:]
            
            #render phrase
            if self.lastI1[4:] == Register(b"1100"):
                #this is a string of LDI's only first counts others are nop
                instcode="NOP"
                instphrase = instcode+"\t"+"(series of LB's"
                return instphrase
            else:
                instcode="LB"
                instphrase = instcode+"\t"+"{0:02X}".format((~self.I2).toInt())
                return instphrase


        self.P = incr(self.P[:6])+self.P[6:]
        return ""
    
if __name__ == '__main__':
    fb = open("A1752EFA1753EE.bin", "rb")
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
    for i in range(4096):
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
                print("****************************")
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

    