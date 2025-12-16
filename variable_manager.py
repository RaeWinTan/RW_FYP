"""

"""

#the variables will be a list of numbers
#just permute accordingly

from typing import List
from collections import deque 


"""
arr: mat 
n: # rows
m: # cols 
trr: left rotation per row
"""

"""
example of (4,4, [0,1,2,3])
[
0, 1, 2 ,3
5, 6, 7, 4
10, 11, 8, 9
15, 12, 13, 14
]
"""
#we want to generate permutations on the fly as well 

def transpose(n):
    rtn = [i for i in range(n*n)]
    for r in range(n):
        for c in range(r):
            rtn[r*n + c], rtn[c*n + r] = rtn[c*n + r], rtn[r*n + c]
    return rtn 
    

#shift than tranpose
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
