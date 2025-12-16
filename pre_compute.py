"""
The aims is given given a fixed nxn matrix "mc" and an arbitrary nxn matrix "state". 
Give me a fast way to compute the matrix multiplication.
"""

from typing import List


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
    #we assume the user will use multiply like: state * mc 
    #so the user must be smart about mc he may need to transpose before inputing
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
    def multiply(self, state:List[int]):
        #NOTE: this means state * mc NOT mc * state 
        rows = [0]*self.n #n words 
        for r in range(self.n):
            #store (be acc) 4 tmp variables each one bytes in one contiguous array
            #acc^=self.tables[c][state[r*self.n+c]]
            #after the c for loop
            #update the state acorrdingly
            for c in range(self.n):
                rows[r] ^= self.tables[c][state[r*self.n + c]]
        rtn = [] 
        for r in range(self.n):
            rtn.extend(list(rows[r].to_bytes(self.n, "big")))
        return rtn

"""
SHOULD HAVE ANOTHER CLASS CALLED COMPILER 

what the compiler will do is:



"""