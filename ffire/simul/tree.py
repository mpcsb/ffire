# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""

import numpy as np
# import matplotlib.pyplot as plt

class Tree():
    def __init__(self, tree_params, lat_lon, x_y):
        h = tree_params['type']['height']
        self.height = np.random.normal(h, h * 0.2) # should be weibul
        self.type = tree_params['type'] 
        self.fuel_perc = self.height * np.random.normal(10, 1) # how burnt the tree is

        self.state = 'unburnt'  
        self.lat_lon = lat_lon
        self.x_y = x_y

    def __eq__(self, other_tree):
        return self.lat_lon == other_tree.lat_lon

    def __hash__(self):
        return hash(self.lat_lon)
