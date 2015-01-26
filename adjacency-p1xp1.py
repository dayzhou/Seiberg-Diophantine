#!/usr/bin/env python3
'''
First calculate all possible adjacency matrices dual
to P1xP1 quiver. Then abstract non-vanishing entries
from each matrix to form an edge combination. All
this combinations form a Seiberg Dual database. This
database will be used to compare to those combinations
obtained from solving the Diophantine equation. This
database in stored in a file called 'database.txt'.

There are two input parameters. The first is the level
parameter which tells the program how many levels you
want to perform the Seiberg dual operation to the base
adjacency matrix. The second is the maximum number
parameter which is optional and has a default value
2000 if not given. This parameter tells the program
not to care about those dual matrices that has entries
greater than the max value.

===== ===== License: MIT ===== =====
'''

import sys
import os

OUTPUT = 'database.txt'

def sbg_dual(adj, i0):
    def edual(i, j):
        return adj[i][j] - adj[i0][i] * adj[j][i0]
    
    nodes = len(adj)
    return tuple([ tuple([ adj[j][i] if (i == i0) or (j == i0)
        else (edual(i, j) if edual(i, j) >= 0 else 0)
            if (i != i0) and (j != i0) and (adj[i0][i] != 0) and (adj[j][i0] != 0)
        else adj[i][j] - edual(j, i)
            if (i != i0) and (j != i0) and (adj[i][i0] != 0) and (adj[i0][j] != 0) and (edual(j, i) < 0)
        else adj[i][j]
        for j in range(nodes) ])
        for i in range(nodes) ])


def flatten(adj):
    return [ e for es in adj for e in es ]

def select(pred, lst, n=0):
    if n == 0:
        return [ e for e in lst if pred(e) ]
    else :
        i, res = 0, []
        for e in lst:
            if pred(e):
                res.append(e)
                i += 1
            if i == n:
                break
        return res


def transv_duals(adj, lv, mx):
    nodes = len(adj)
    preAdjs = currAdjs = []
    adjs = [adj]
    
    def get_combi(a):
        temp = select(lambda e: e != 0, flatten(a))
        temp.sort()
        return tuple(temp)
    
    def below_mx(a):
        return select(lambda x: x > mx, flatten(a), 1) == []
    
    def duals(a):
        return select(below_mx, map(lambda i: sbg_dual(a, i), range(nodes)))
    
    def new_adjs(ads):
        return select(lambda a: a not in preAdjs, ads)
    
    def new_combis(combis):
        return set(select(lambda c: c not in lst, combis))
    
    lst = {get_combi(adj)}
    for j in range(lv):
        preAdjs = currAdjs
        currAdjs = adjs
        adjs = new_adjs(set([ a for ads in map(duals, currAdjs) for a in ads]))
        lst |= new_combis(set(map(get_combi, adjs)))
    
    return lst


if __name__ == '__main__':
    B1 = ((0, 2, 0, 0), (0, 0, 2, 0), (0, 0, 0, 2), (2, 0, 0, 0))
    
    try:
        level = int(sys.argv[1])
        try:
            mx = int(sys.argv[2])
        except:
            mx = 2000
        
        os.chdir(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(OUTPUT, 'w') as fl:
            for combi in transv_duals(B1, level, mx):
                fl.write(str(combi) + '\n')
    except:
        print('\nGive me the level number\n')
