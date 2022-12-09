'''
Created on 6 déc. 2022

@author: garzol
'''



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
