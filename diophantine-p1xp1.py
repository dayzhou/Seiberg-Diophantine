#!/usr/bin/env python3
'''
Solve the Diophantine equation level by level. Each
level has width = 20, which means we first solve the
equation by finding all solutions whose components
are less than or equal to 20, then 40, 60, etc. In
the above solving process we only care about even
solutions. After having solved one level, all solutions
obtained in this level will be append to a file named
'solutions.txt'.

There are two input parameters. The first is the level
parameter with 20 as a unit and starting from 0 which
means the program will compute all solutions less than
200 if setting the level to 9. The second parameter is
the number of process parameter with a default value of
4 if not given. This parameter is to maximize the efficiency
of computing if the program is running on a multi-core
machine. We suggest this value be the number of cores
if the machine is only for computation use.

===== ===== License: MIT ===== =====
'''

import sys
import os
import time
from multiprocessing import Pool, Manager
from functools import wraps

OUTPUT = 'solutions.txt'
lvGap = 20

# Timer
def timer(func) :
    '''timing function wrapper'''
    @wraps(func)
    def _timing(*args, **kargs) :
        begin, sBegin= time.time(), time.ctime()
        res = func(*args, **kargs)
        end, sEnd = time.time(), time.ctime()
        print('\nTime begins at: %s' % sBegin)
        print('Time ends at: %s' % sEnd)
        print('Time lapse: %g sec\n' % (end - begin))
        return res
    return _timing


def dioph(a, b, c, d, e):
    return (a**2 * b**2) + (a**2 * c**2) + (b**2 * c**2) \
        + (c**2 * d**2) + (c**2 * e**2) + (d**2 * e**2) \
        + (c**4) - (a**2 * b**2 * c**2) + (b * c**3 * d) \
        - (a * c**3 * e) + (a * b**2 * c * e) - (a**2 * b * c * d) \
        + (2 * a * b * d * e) - (a * c * d**2 * e) \
        + (b * c * d * e**2) - (a * b * c**2 * d * e)


def solutions(aRng, bRng, cRng, dRng, eRng):
    return [ (a, b, c, d, e, int((a*b + d*e)/c))
        for a in aRng
        for b in bRng
        for c in cRng
        for d in dRng
        for e in eRng
        if c**2 <= a*b + d*e and dioph(a, b, c, d, e) == 0 ]


def next_seq(lv, seq):
    p, q, i, j, k = seq
    k = (k + 1) % (lv + 1)
    if k == 0:
        j = (j + 1) % (lv + 1)
        if j == 0:
            i = (i + 1) % (lv + 1)
            if i == 0:
                q = (q + 1) % (lv + 1)
                if q == 0:
                    p += 1
    
    if lv in (p, q, i, j, k):
        return (p, q, i, j, k)
    else :
        return next_seq(lv, (p, q, i, j, k))


def toRanges(seq):
    def _range(i, lv):
        if lv == 0 and i != 2:
            return range(0, lvGap + 1, 2)
        else:
            return range(lvGap * lv + 2, lvGap * (lv + 1) + 1, 2)
    
    return [ _range(i, lv) for i, lv in enumerate(seq) ]


def rangesStream(lv, start=None):
    if start == None:
        nxt = (0, 0, 0, 0, lv)
    else:
        nxt = start
    
    yield (nxt, queue)
    while nxt != (lv, lv, lv, lv, lv):
        nxt = next_seq(lv, nxt)
        yield (nxt, queue)


def handle_sols(rngs):
    rng, q = rngs
    print()
    for s in solutions(*toRanges(rng)):
        print('Solution: %s' % str(s))
        q.put(s)
    print('===> Done computing: %s' % str(rng))


@timer
def compute(rngsStrm, droids=4):
    with Pool(processes=droids, maxtasksperchild=10) as pool:
        pool.map(handle_sols, rngsStrm)


if __name__ == '__main__':
    try:
        level = int(sys.argv[1])
        try:
            robots = int(sys.argv[2])
        except:
            robots = 4
        
        queue = Manager().Queue()
        compute(rangesStream(level), droids=robots)

        os.chdir(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(OUTPUT, 'a') as fl:
            try:
                while True:
                    fl.write(str(queue.get(block=False)) + '\n')
            except:
                fl.write('# UP TO %d\n\n' % (lvGap * (level + 1)))
    except ValueError:
        print('\nGive me the level number\n')
