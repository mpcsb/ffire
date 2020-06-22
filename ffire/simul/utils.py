# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 23:14:50 2020

@author: Miguel
"""
import math
from math import sqrt
import unittest

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
         
        if p3 - q3 <= 0: # burning tree is below other trees
            p_2d = (p[0], p[1])
            q_2d = (q[0], q[1])
            return dist(p_2d, q_2d)
        if p3 - q3 > 0: # burning tree is above other trees
            return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
        

def bearing(p1, p2):
    lat1, lon1 = p1
    lat2, lon2 = p2
    
    lat1 = lat1 * math.pi / 180;
    lat2 = lat2 * math.pi / 180;
    dLon = (lon2-lon1) * math.pi / 180;
    y = math.sin(dLon) * math.cos(lat2);
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2)  *math.cos(dLon);

    bearing = math.atan2(y, x) * 180 / math.pi;
    if bearing < 0:
        bearing = bearing + 360;
         
    return bearing
 

def sigmoid(x):
  return 1 / (1 + math.exp(-x))



class TestUtils (unittest.TestCase):

    def test_dist(self):
        p = (1, 2, 3)
        q = (3, 4, 5)
        self.assertEqual(dist(p, q), 2.8284271247461903) 
        self.assertEqual(dist(q, p), 3.4641016151377544) 