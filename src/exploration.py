# -*- coding: utf-8 -*-
"""
Created on Mon May 25 21:30:16 2020

@author: Miguel
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
#%%

params = {
  "forestColor": "green",
  "fireColor": "red",
  "emberColor": "yellow",
  "lightningColor": "silver",
  "forestDensity": 0.1,
  "forestHeight": 10,
  "emberHeight": 2,
  "lightningChance": 0.001,
  "regrowthChance": 0.01,
  "wildfire_count": 10,
  "topology": {
    "x_bounds": [-0, 10],
    "y_bounds": [-0, 10],
    "search_radius": 1
  }
}



class tree():
    
    def __init__(self, forestHeight, x, y):
        self.height = np.random.normal(forestHeight, 3)
        self.fire = False
        self.ember = False
        self.coords = x, y
    
    def burn(self):
        # a tree must not be burnt before burning
        if self.ember == True:
            pass
        else:
            self.fire = True

    def turn_ember(self):
        if self.fire == True:
            self.ember = True
            self.fire = False
            


class forest():
    
    def __init__(self, params):
        self.grid = [[tree(params["forestHeight"], x, y) for x in range(params["topology"]["y_bounds"][0], 
                                    params["topology"]["y_bounds"][1])] 
                  for y in range(params["topology"]["x_bounds"][0],
                                 params["topology"]["x_bounds"][1])]
    
    def plot(self):
        # Data generation
        alpha = np.linspace(1, 8, 5)
        t = np.linspace(0, 5, 16)
        T, A = np.meshgrid(t, alpha)
        data = np.exp(-T * (1. / A))
        
        # Plotting
        fig = plt.figure()
        ax = fig.gca(projection = '3d')
        
        Xi = T.flatten()
        Yi = A.flatten()
        Zi = np.zeros(data.size)
        
        dx = .25 * np.ones(data.size)
        dy = .25 * np.ones(data.size)
        dz = data.flatten()
        
        ax.set_xlabel('T')
        ax.set_ylabel('Alpha')
        ax.bar3d(Xi, Yi, Zi, dx, dy, dz, color = 'w')
        
        plt.show()     
        
    # def propagate_fire(self):
    #     coords = [(r,c) for r in range(height) for c in range(width)]
    #     for rc in coords:
    #         r, c = rc
            
