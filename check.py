#!/usr/bin/env python3
'''
Check whether all even solutions obtained by solving the
Diophantine equation are in the Seiberg duals and output
those not in the Seiberg duals to a file named 'exceptions.txt'.

===== ===== License: MIT ===== =====
'''

import os

combisFile = 'database.txt'
solsFile = 'solutions.txt'


def sort(lst):
    lst.sort()
    return lst


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


def read_combis():
    with open(combisFile, 'r') as f:
        combis = {eval(c) for c in f}
    return combis


def read_sols():
    with open(solsFile, 'r') as f:
        sols = [ tuple(sort(select(lambda e: e != 0, eval(s))))
            for s in f
            if s.strip('\n') and not s.startswith('#') ]
    return sols


def main():
    combis = read_combis()
    sols = read_sols()
    
    with open('exceptions.txt', 'w') as f:
        for sol in sols:
            if sol not in combis:
                print(sol)
                f.write(str(sol) + '\n')


if __name__ == '__main__':
    os.chdir(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    main()
    
