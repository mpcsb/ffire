# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""
import numpy as np
import matplotlib.pyplot as plt
import random
import utm
from functools import lru_cache

from simul.terrain import Terrain

from simul.tree import Tree
from simul.utils import dist
 

class Forest:

    def __init__(self, params):
        self.terrain = Terrain(params['terrain_params'])
        self.shape = params['terrain_params']['shape']

        # self.wind = Wind(params['weather_params'])
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
        
        self.sampled_trees = random.sample(self.tree_lst, 20000)


    def _forest_gen(self, tree_params):
        ''' generate collection of trees over the terrain '''
        
        p1, p2 = self.shape 
        x0, y0,_, _ = utm.from_latlon(p1[0], p1[1])
        
        np_lat = np.linspace(p1[0], p2[0], num=self.terrain.width, endpoint=True)
        np_long = np.linspace(p1[1], p2[1], num=self.terrain.length, endpoint=True)
        coords_lat_lon = [(lat, long) for lat in list(np_lat) for long in list(np_long)]
        
         
        self.tree_lst = list()
        for lat_lon in coords_lat_lon:  
            if random.random() > self.forest_density:
                lat, lon = lat_lon
                
                x, y, _, _ = utm.from_latlon(lat, lon)
                x -= x0
                y -= y0
                
                altitude = self.terrain.interpolated_lat_lon_alt(lat, lon)
                altitude_cart = self.terrain.interpolated_cartesian(x, y)
                
                lat_lon_alt = (lat, lon, int(altitude[0]))
                x_y_alt = (x, y, int(altitude_cart[0]))
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
            try:
                self.quadrants[x // d][y // d].append(t)
            except:
                print(x, y)


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
                  'ash':'grey'}
 
        coords = [t.lat_lon for t in self.sampled_trees]
        x_y = [t.x_y for t in self.sampled_trees]

        color = [colors[t.state] for t in self.sampled_trees] 
        lat, lon, z = list(map(list, zip(*coords)))
        x, y, z = list(map(list, zip(*x_y))) 

        ax1 = plt.subplot(212) 
        ax1.scatter(lat, lon, c=color, s=2, alpha=0.3)
        
        ax2 = plt.subplot(221) 
        ax2.scatter(lat, lon, c=z, s=2, alpha=0.3)
        ax2.set_title('Lat Long')
        # plt.colorbar(ax2)
        
        ax3 = plt.subplot(222) 
        ax3.scatter(y, x, c=z, s=3, alpha=0.3)
        ax3.set_title('Meters') 
        # plt.colorbar(ax3)
 

    def reset_forest(self, params):
        ''' aux method to replicate simulation '''
        self._forest_gen(params['tree_params'])

#%%

 