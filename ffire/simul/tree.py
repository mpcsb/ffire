# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""

import numpy as np
# import matplotlib.pyplot as plt

class Tree():
    def __init__(self, tree_params, coord):
        h = tree_params['type']['height']
        self.height = np.random.normal(h, h * 0.2)
        self.type = tree_params['type'] # dict containing properties of tree:
                                   # species name, radius, burn ability, ...
        self.fuel_perc = self.height * np.random.normal(10, 1) # how burnt the tree is

        self.state = 'unburnt' # burning, ember, charcoal
        # self.safe_radius = tree_params['safe_radius'] # https://www.tandfonline.com/doi/full/10.1080/21580103.2016.1144541
        self.coord = coord

    def __eq__(self, other_tree):
        return self.coord == other_tree.coord

    def __hash__(self):
        return hash(self.coord)
