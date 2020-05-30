# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""

import matplotlib.pyplot as plt

from terrain import Terrain
from tree import Tree


class Forest:
    
    def __init__(self, params):
        forest_params = params['forest_params']
        terrain_params = params['terrain_params']
        tree_params = params['tree_params']
        
        self.forest_density = forest_params['forest_density']
        self.forest_mixture = forest_params['forest_mixture']
        self.terrain = Terrain(terrain_params)
        
        self.forest = self._forest_gen(tree_params)
        

    def _forest_gen(self, tree_params):
        ''' generate collection of trees over the terrain '''
        self.tree_lst = list()
        for coord in self.terrain.shape:
            self.tree_lst.append(Tree(tree_params, coord))


    def plot(self):
        height_distribution = [t.height for t in self.tree_lst]
        plt.hist(height_distribution, bins='auto')
 

#%%
 