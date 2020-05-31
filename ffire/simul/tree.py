# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""

import numpy as np
# import matplotlib.pyplot as plt 

class Tree():
    def __init__(self, params, coord):
        h = params['type']['height']
        self.height = np.random.normal(h, h * 0.2)
        self.type = params['type'] # dict containing properties of tree:
                                   # species name, radius, burn ability, ...
        self.fuel_perc = params['fuel_perc'] # how burnt the tree is
        self.ember = params['ember']
        self.burning = params['burning']
        self.coord = coord

    # def _sample_height(h=11):
    #     # http://blogs.oregonstate.edu/geog566spatialstatistics/2019/04/19/point-pattern-analysis-of-tree-distribution-by-height-in-the-hj-andrews-forest/
    #     return np.random.normal(h, h * 0.2)
