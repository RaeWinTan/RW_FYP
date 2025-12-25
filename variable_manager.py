from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Union, List
from collections import deque 

IndexKey = Union[int, slice, tuple, list]

@dataclass(frozen=True)
class IndexedOperand:
    src: "Variable"
    idxs: tuple[int, ...]

class Variable:
    def __init__(self,n):
        self.n = n 
        self.vals = [0]*n 
    def __getitem__(self, key):
        return self.vals[key]
    def __setitem__(self,key,value):
        if isinstance(key, list):
            for i in range(len(key)):
                self.vals[self.key[i]]= value[i]
        else:
            self.vals[key] = value 
    def __ixor__(self, other):
        if isinstance(other, IndexedOperand):
            src, idxs = other.src, other.idxs 
            if self.n == len(other.idx): #for the case of aes expaneded key ^ state
                for i in range(self.n):
                    self[i] = self[i] ^ src[idxs[i]]
            else:#usually means one guy is string integers the other bytes
                raise NotImplementedError("TO BE DONE FOR MULTIPLY I THINK")
        if isinstance(other, Variable):
            if self.n==other.n:
                for i in range(self.n):
                    self[i] = self[i] ^ other[i]
            else:#usually means one guy is storing integeres the other bytes
                raise NotImplementedError("TO BE DONE FOR MULTIPLY I THINK")
        return self 

class StateVariable(Variable):#we will be placing these in regester (128,256)
    def __init__(self,n):
        super().__init__(n)
        self.perm = [i for i in range(n)]
    def set_perm(self, prr):
        self.perm = reassign(self.perm,prr)
    def __getitem__(self, key):
        if isinstance(key, list):
            return IndexedOperand(self, key)
        return super().__getitem__(self.perm[key])
    def __setitem__(self, key, value):
        if isinstance(key,list):
            super().__setitem__([self.perm[k] for k in key], value)
        else:
            super().__setitem__(self.perm[key], value)
    def reassign(self):
        rtn = [-1]*self.n 
        for i in range(self.n):
            rtn[i] = self.vals[self.perm[i]]
        self.vals = rtn 
        self.perm = [i for i in range(self.n)]
    def load_values(self, other:StateVariable):
        """
        need to take care of self.n != other.n 
        For now just assum self.n =16 while other.n = 4
        """
        pass 
    
class ConstVariable(Variable):
    def __init__(self,n, vals):
        super().__init__(n)
        self.vals = vals.copy()



"""
For constvarialbes:
    - this is will not be in register. i will be my look up 
    - whenever it gets called in code it will just return hm[singulre varialbe item]
    - perhap that 
For state varialbes there wil lbe two types of presentaiton in the CPP
code. 
Type 1: each variable is in register. want it to stay there as much as posible
        - state is a good candidate
Type 2: there will be times where it gets split up because we are doing hash table look ups
        - 

you see the logic for permuting is the exact same it is only 
how it should be presented and how it would 
operate basic variables
- so like lets say you will be 
operation aginast a vector and all i have it is bytes
a smart move its t

should operations should be outside of variable?

or like staet[[0,1,2,3,4,5,6,7]]^= otherState[[0,1,2,3,4,5,6,7]]

for now just handle otherState is the expanded key 
the state is state
OtherState of type no in register
state is of type register




for key expansion the variables should be held in that many variables thing for the most part 

on at add_round_key

state^=subset of key variabels

so over ixor should have 


"""
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
