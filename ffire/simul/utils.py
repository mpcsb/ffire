# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 23:14:50 2020

@author: Miguel
"""

from math import sqrt

def dist(p, q):
    '''
    p = (1, 2, 3)
    q = (3, 4, 5)

    >>> dist(p,q)
    2.8284271247461903
    >>> dist(q,p)
    3.4641016151377544
    '''
    if len(p) == 2:
        return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
    
    if len(p) == 3:
        _, _, p3 = p
        _, _, q3 = q
         
        if p3 - q3 <= 0:
            p_2d = (p[0], p[1])
            q_2d = (q[0], q[1])
            return dist(p_2d, q_2d)
        if p3 - q3 > 0: # burning tree is above other trees
            return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))