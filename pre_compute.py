"""
The aims is given given a fixed nxn matrix "mc" and an arbitrary nxn matrix "state". 
Give me a fast way to compute the matrix multiplication.
"""

from typing import List
from variable_manager import VariableManager

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
    
    def __init__(self, mc:List[int],sbox:List[int], n:int):
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

    #solve a word at a time 
    #NOTE: this means state * mc NOT mc * state 
    def multiply(self, state:VariableManager):
        other = VariableManager(self.n)#array of 32bit objects
        for r in range(self.n):
            for c in range(self.n):
                other.set_val(r, other.get_val(r)^self.tables[c][state.get_val(r*self.n + c)])
        state.load_values(other)
        #optimize for good COMPILED performance later 
        
"""

MULTIPLY:
each hm[i][j] is a 32 bit word
hm[0][b0]^hm[1][b1]^hm[2][b2]^hm[3][b3] = [c0, c1, c2, c3]
hm[0][b4]^hm[1][b5]^hm[2][b6]^hm[3][b7] = [c4, c5, c6, c7]
hm[0][b8]^hm[1][b9]^hm[2][b10]^hm[3][b11] = [c8, c9, c10, c11]
hm[0][b12]^hm[1][b13]^hm[2][b14]^hm[3][b15] = [c12, c13, c14, c15]

SHOULD HAVE ANOTHER CLASS CALLED COMPILER 
"""