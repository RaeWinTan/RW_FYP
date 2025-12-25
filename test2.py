from dataclasses import dataclass
from typing import Iterable, Union

IndexKey = Union[int, slice, tuple, list]

@dataclass(frozen=True)
class IndexedOperand:
    src: "Variable"
    idxs: tuple[int, ...]

class Variable:
    def __init__(self, n: int, name:str="someName"):
        self.n = n
        self.vals = [0] * n
    
    def _get(self,i):
        return self.vals[i]

    def _set(self,i):
        return self.vals[i]
    

    def __getitem__(self, key: IndexKey):
        # normal element access
        return self.vals[key]

    def __setitem__(self, key: IndexKey, value):
        # support batch set: v[[1,2,3]] = [a,b,c] or v[(1,2,3)] = [...]
        if isinstance(key, (list, tuple)):
            if len(key) != len(value):
                raise ValueError("key/value length mismatch")
            for k, v in zip(key, value):
                self.vals[k] = v
        else:
            self.vals[key] = value

    def __ixor__(self, other):
        if isinstance(other, IndexedOperand):
            src, idxs = other.src, other.idxs
            for i in range(self.n):
                self[i] = self[i] ^ src[idxs[i]]   # write-back is important
            return self

        # optional: allow full-vector xor
        if isinstance(other, Variable):
            if self.n != other.n:
                raise ValueError("size mismatch")
            for i in range(self.n):
                self[i] = self[i] ^ other[i]
            return self

        return NotImplemented

class ConstVariable(Variable):


class RegisterVariable(Variable):
    pass 

class IndividualVariable(Variable):
    pass 



class StateVariable(Variable):
    def __init__(self, n: int):
        super().__init__(n)
        self.perm = list(range(n))

    def set_perm(self, prr: Iterable[int]):
        prr = list(prr)
        if len(prr) != self.n:
            raise ValueError("perm length mismatch")
        self.perm = prr

    def __getitem__(self, key: IndexKey):
        # KEY PART: if key is list/tuple -> return an operand that carries indices
        if isinstance(key, (list, tuple)):
            #idxs = tuple(self.perm[k] for k in key)
            return IndexedOperand(self, key)

        # normal element access
        return super().__getitem__(self.perm[key])

    def __setitem__(self, key: IndexKey, value):
        if isinstance(key, (list, tuple)):
            real = [self.perm[k] for k in key]
            super().__setitem__(real, value)
        else:
            super().__setitem__(self.perm[key], value)

var = Variable(8)
state = StateVariable(8)
state.vals = [j for j in range(1, 9)]
vm = StateVariable(8)
vm.vals = [1,2,3,4,5,6,7,8]
vm.perm = [7,6,5,4,3,2,1,0]
ek_vm_ids = list(range(8))
state ^= vm[tuple(range(8))]  
print(state.vals)
