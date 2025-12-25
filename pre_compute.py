"""
The aims is given given a fixed nxn matrix "mc" and an arbitrary nxn matrix "state". 
Give me a fast way to compute the matrix multiplication.
"""

from typing import List
from variable_manager import VariableManager, ConstVariable, StateVariable, Variable

class Matrix:
    @staticmethod
    def transpose(arr,n):
        for r in range(n):
            for c in range(r+1,n):
                arr[r*n + c], arr[c*n+r] = arr[c*n+r],arr[r*n+c]
    @staticmethod
    def gmul(a,b):
        p = 0
        for c in range(8):
            if b & 1:
                p ^= a
            carry = a & 0x80
            a <<= 1
            if carry:
                a ^= 0x11b
            b >>= 1
        return p
    
    @staticmethod
    def getRc(x, n):
        return (x//n, x%n)

    @staticmethod
    def getX(r,c,n):
        return r*n + c 

class FastMultiply:
    
    def __init__(self, mc:List[int],sbox:ConstVariable, n:int):
        #we want mc to be on the left always and we assume that plaintext is given in a row-wise 
        #solve a row at a time
        self.mc = mc 
        self.n = n
        #precalculate self.n tables, we assume it is a GF(2^3) multiplication
        self.tables = [[0]*256 for _ in range(self.n)]#each value has self.n bytes
        for t in range(self.n):
            for num in range(256):
                tmp = [] 
                for c in range(self.n):#take the row of the mc
                    con = self.mc[t*self.n + c]
                    tmp.append(Matrix.gmul(sbox[num],con))
                self.tables[t][num] = int.from_bytes(bytes(tmp), "big")
        #should specify that each item in each constvariables is an integer not a byte
        self.tables_const:list[ConstVariable] = [ConstVariable(256, self.tables[t]) for t in range(self.n)]
        
    #solve a word at a time 
    #NOTE: this means state * mc NOT mc * state 
    def multiply(self, state:VariableManager):
        #wise to just put it at init so now only one variable is played with the whole program
        other = VariableManager(self.n)#array of 32bit objects, this variable manager also need to make chages
        #this should this logic be in variables object?
        """
        let v be the state variable that is in register
        uint8_t bytes[16];
        _mm_storeu_si128((__m128i*)bytes, v);
        should look like 
        uint32 b0,b1,b2,b3     =    bytes[p0],bytes[p1]...
        b4,b5,b6,b7            =    ...
        b8,b9,b10,b11          =    ...
        b12,b13,b14,b15        =    ...

        b0,b1,b2,b3     =  table0[b0], table1[b1]....
        b4,b5,b6,b7     = table0[b4], table1[b5]...
        b8,b9,b10,b11   =...
        b12,b13,b14,b15 = table0[b12].....table3[b15]
        
        #tme varaibles for my other be
        w1 = b0^b1^b2^b3
        w2 = b4^b5^b6^b7
        w3 = ...
        w4 = b12^....^b15
        other = __mm__...(w1,w2,w3,w4)#store in to register
        
        """
        for r in range(self.n):
            for c in range(self.n):
                other[r] = other[r] ^ self.tables_const[c][state[r*self.n + c]]
                #other.set_val(r, other.get_val(r)^self.tables[c][state.get_val(r*self.n + c)])
        state.load_values(other)
        
        
"""

MULTIPLY:
each hm[i][j] is a 32 bit word
hm[0][b0]^hm[1][b1]^hm[2][b2]^hm[3][b3] = w1
hm[0][b4]^hm[1][b5]^hm[2][b6]^hm[3][b7] = w2
hm[0][b8]^hm[1][b9]^hm[2][b10]^hm[3][b11] = w3 
hm[0][b12]^hm[1][b13]^hm[2][b14]^hm[3][b15] = w4

how to do it in parallise it?

SHOULD HAVE ANOTHER CLASS CALLED COMPILER 
"""