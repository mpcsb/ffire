# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""
import numpy as np
import matplotlib.pyplot as plt
import random
# import copy
from functools import lru_cache

from simul.terrain import Terrain
from simul.weather import Wind, Humidity
from simul.tree import Tree
from simul.utils import dist
 

class Forest:

    def __init__(self, params):
        self.terrain = Terrain(params['terrain_params'])
        self.shape = params['terrain_params']['shape']
        self.wind = Wind(params['weather_params'])
        # self.humidity = Humidity(params['weather_params'])
        
        self.forest_density = params['forest_params']['forest_density']
        self.forest_mixture = params['forest_params']['forest_mixture']
        self.safe_radius = params['forest_params']['safe_radius']

        self._forest_gen(params['tree_params'])
        self._quadrant_gen()
        self._nearest_trees()
        self._coord2tree()

        self.tree_state = {'unburnt': set(self.tree_lst),
                           'burning':set(),
                           'burning_recent':set(),
                           'ember':set(),
                           'ash':set()
                           }



    def _forest_gen(self, tree_params):
        ''' generate collection of trees over the terrain '''
        
        p1, p2 = self.shape
        
        coords_x_y = [(r, c) for r in range(self.terrain.width) for c in range(self.terrain.length)]
        
        np_lat = np.linspace(p1[0], p2[0], num=self.terrain.length, endpoint=True)
        np_long = np.linspace(p1[1], p2[1], num=self.terrain.width, endpoint=True)
        coords_lat_lon = [(lat, long) for lat in list(np_lat) for long in list(np_long)]
        
        self.tree_lst = list()
        for lat_lon, x_y in zip(coords_lat_lon, coords_x_y): #TODO assert this is valid and generalizes
            if random.random() > self.forest_density:
                lat, lon = lat_lon
                x, y = x_y
                altitude = self.terrain.interpolated_lat_lon_alt(lat, lon)
                # altitude = self.terrain.interpolated_cartesian(x, y)
                
                lat_lon_alt = (lat, lon, int(altitude[0]))
                x_y_alt = (x, y, int(altitude[0]))
                self.tree_lst.append(Tree(tree_params, lat_lon_alt, x_y_alt))

        print(f'{len(self.tree_lst)} trees in selected area')
        print(f'{self.terrain.length * self.terrain.width} square meters in selected area')


    def _quadrant_gen(self):
        ''' 
        which points belong to which quadrant reduces computation
        '''
 
        d = self.safe_radius
        self.quadrants = {x: {y: list() for y in range(int((self.terrain.length + 1) // d + 1))}
                          for x in range(int((self.terrain.width + 1) // d + 1))}

        for t in self.tree_lst:
            x, y, _ = t.x_y
            self.quadrants[x // d][y // d].append(t)


    def _nearest_trees(self):
        ''' generates a dictionary with the nearest trees up to a distance '''
        self.neighbours = dict()
        
        for t1 in self.tree_lst:
            x, y, _ = t1.x_y
            x = x // self.safe_radius
            y = y // self.safe_radius

            comparable_trees = self.__adjacent_trees(x, y)
            
            for t2 in comparable_trees:
                d = dist(t1.x_y, t2.x_y)
                
                if 0.0 < d < self.safe_radius:
                    if t1 in self.neighbours.keys():
                        self.neighbours[t1].append((d, t2))
                    else:
                        self.neighbours[t1] = [(d, t2)]


    @lru_cache()
    def __adjacent_trees(self, x, y):
        ''' receives quadrant coords and returns list of potential burning trees'''
        comparable_trees = list()
        diffs = [(dx, dy) for dx in range(-2, 2) for dy in range(-2, 2)]

        for delta in diffs:
            dx, dy = delta
            try:
                t_lst = self.quadrants[x + dx][y + dy]
                comparable_trees.extend(t_lst)
            except KeyError:
                continue

        return comparable_trees


    def _coord2tree(self):
        ''' mapping from coordinate to tree '''
        self.coord_dict = dict()
        for t in self.tree_lst:
            self.coord_dict[t.lat_lon] = t
            self.coord_dict[t.x_y] = t


    def tree_feature_distribution(self, feature):
        height_distribution = [t.feature for t in self.tree_lst]
        plt.hist(height_distribution, bins='auto')


    def plot(self):
        colors = {'unburnt':'green',
                  'burning':'red',
                  'ember':'orange',
                  'ash':'black'}
        # def size_tree(h):
        #     if h>12:
        #         return 2
        #     else:
        #         return 1

        coords = [t.lat_lon for t in self.tree_lst]
        color = [colors[t.state] for t in self.tree_lst]
        # size = [size_tree(t.height) for t in self.tree_lst]
        x, y, z = list(map(list, zip(*coords)))
        
        fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 1]})
        axs[0].scatter(x, y, c=color, s=2, alpha=0.3)
        axs[1].scatter(x, y, c=z, s=2, alpha=0.3)



    def reset_forest(self):
        ''' aux method to replicate simulation '''
        self.tree_state = {'unburnt': set(self.tree_lst),
                           'burning':set(),
                           'burning_recent':set(),
                           'ember':set(),
                           'ash':set()
                           }        
        for t in self.tree_lst:
            t.state = 'unburnt'

#%%
 