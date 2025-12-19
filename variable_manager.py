from __future__ import annotations
from typing import List
from collections import deque 

class VariableManager:
    def __init__(self,n):#n is the size of the 1d array 
        self.vals = [0]*n 
        self.perm = [i for i in range(n)]
        self.n = n 
    def set_perm(self,prr):
        self.perm = reassign(self.perm, prr) 
    def set_val(self, idx,val):#can set a operator as well
        self.vals[self.perm[idx]] = val 
    def get_val(self, idx):
        return self.vals[self.perm[idx]]
    def reassign(self):
        rtn = [-1]*self.n 
        for i in range(self.n):
            rtn[i] = self.vals[self.perm[i]]
        self.vals = rtn 
        self.perm = [i for i in range(self.n)]
    def load_values(self, other:VariableManager):
        #so if the other length is like 4 time smaller we do it differently
        if other.n < self.n:
            #in implementaiton it should look something like
            #_m128i currState = _mm_setr_epi8(..... 16 objects)//already given
            #_m128i otherState = _mm_setr_epi32(.....4 objects)//algirth given
            # need to bytepermute otherState first -> currState=otherState
            # currState= other// 
            for r in range(other.n):
                for c in range(other.n):
                    self.set_val(r*other.n + c, (other.get_val(r)>>((3-c)*8) )&0xff )
            return 
        else:
            for i in range(self.n):
                self.vals[self.perm[i]] = other.vals[other.perm[i]]
    def print_state(self):
        rtn = []
        for i in range(self.n):
            rtn.append(self.vals[self.perm[i]])
        for c in range(4):
            tmp = [] 
            for r in range(4):
                tmp.append(hex(rtn[r*4+c]))
            print(tmp)

def transpose(n):
    rtn = [i for i in range(n*n)]
    for r in range(n):
        for c in range(r):
            rtn[r*n + c], rtn[c*n + r] = rtn[c*n + r], rtn[r*n + c]
    return rtn 

def matrixRotLeft(n:int, trr:List[int]=[0,1,2,3]):
    assert len(trr) == n 
    prr = [i for i in range(n*n)] 
    for r,t in enumerate(trr):
        q = deque(list(range(r*n,(r+1)*n)))
        for _ in range(t): q.append(q.popleft())
        prr[r*n:(r+1)*n] = list(q) 
    return prr #we return the permutation to be used

def reassign(arr, prr):#here reasign to new variables 
    rtn = [-1]*len(arr)
    for i,p in enumerate(prr): rtn[i] = arr[p]
    return rtn 
#need another operator class (perform math operation between two variables)
#all so support between variable and specific value o
#variable manger we all need to split one for runtime variable another 
#for constant variables 
#when come to code implementation
#thie variable manager will take the most hit
#for variable manager: must also set if it is a 8bit object of 32bit object