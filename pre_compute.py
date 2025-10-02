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
            a <<= 1
            if a & 0x100:
                a ^= 0x11b
            b >>= 1
        return p


class FastMultiply:
    #we assume the user will use multiply like: state * mc 
    #so the user must be smart about mc he may need to transpose before inputing
    def __init__(self, mc:List[int], n:int):
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
                    tmp.append(Matrix.gmul(num,con))
                self.tables[t][num] = int.from_bytes(bytes(tmp), "big")


    #solve a word at a time 
    def multiply(self, state:List[int]):
        #NOTE: this means state * mc NOT mc * state 
        rows = [0]*self.n #n words 
        for r in range(self.n):
            for c in range(self.n):
                #two posiblitlies, element in state is a byte or a word(of n bytes)
                rows[r] ^= self.tables[c][state[r*self.n + c]]
        rtn = [] 
        for r in range(self.n):
            rtn.extend(list(rows[r].to_bytes(self.n, "big")))
        return rtn

arr1 = [
    0xd4, 0xe0, 0xb8, 0x1e,
    0xbf, 0xb4, 0x41, 0x27,
    0x5d, 0x52, 0x11, 0x98,
    0x30, 0xae, 0xf1, 0xe5
]

#expected value after mix columns
arr2 = [
    0x04, 0xe0, 0x48, 0x28,
    0x66, 0xcb, 0xf8, 0x06,
    0x81, 0x19, 0xd3, 0x26,
    0xe5, 0x9a, 0x7a, 0x4c
]

mix_col_matrix = [
    0x02, 0x03, 0x01, 0x01,
    0x01, 0x02, 0x03, 0x01,
    0x01, 0x01, 0x02, 0x03,
    0x03, 0x01, 0x01, 0x02
]
n = 4
mc = mix_col_matrix
state = arr1
Matrix.transpose(mc,n)
Matrix.transpose(state,n)
fm = FastMultiply(mc,n)
rtn = fm.multiply(state)
Matrix.transpose(rtn, n)
print(rtn)
assert rtn == arr2

