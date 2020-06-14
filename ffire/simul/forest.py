# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
        try:
            self.sampled_trees = random.sample(self.tree_lst, 5000)
        except:
            self.sampled_trees = self.tree_lst


    def _forest_gen(self, tree_params):
        ''' generate collection of trees over the terrain '''
        
        p1, p2 = self.shape 
        x0, y0,_, _ = utm.from_latlon(p1[0], p1[1])
        
        np_lat = np.linspace(p1[0], p2[0], num=self.terrain.width, endpoint=True)
        np_long = np.linspace(p1[1], p2[1], num=self.terrain.length, endpoint=True)
        coords_lat_lon = [(lat, long) for lat in list(np_lat) for long in list(np_long)]
        
        # minimum point (corner) in initial tile        
        x0, y0,_, _ = utm.from_latlon(self.shape[0][0], self.shape[0][1])
        x1, y1,_, _ = utm.from_latlon(self.shape[1][0], self.shape[1][1])
        min_x = min(x0, x1)
        min_y = min(y0, y1)
         
        self.tree_lst = list()
        for lat_lon in coords_lat_lon:  
            if random.random() > self.forest_density:
                lat, lon = lat_lon
                
                x, y, _, _ = utm.from_latlon(lat, lon)
                x -= min_x
                y -= min_y
                
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
        
        cnt = 0
        total = 0
        for t in self.tree_lst:
            total += 1
            x, y, _ = t.x_y
            try:
                self.quadrants[x // d][y // d].append(t)
            except KeyError: # interpolation gives out of border results: minimal impact
                cnt += 1
        print(f'Quadrant generation: Total:{total}, exceptions:{cnt}')


    def _nearest_trees(self):
        ''' Generates a dictionary with the nearest trees up to a distance '''
        self.neighbours = dict()
        
        for t1 in self.tree_lst:
            x, y, _ = t1.x_y
            x = x // self.safe_radius
            y = y // self.safe_radius

            comparable_trees = self.adjacent_trees(x, y)
            
            for t2 in comparable_trees:
                d = dist(t1.x_y, t2.x_y)
                
                if 0.0 < d < self.safe_radius:
                    if t1 in self.neighbours.keys():
                        self.neighbours[t1].append((d, t2))
                    else:
                        self.neighbours[t1] = [(d, t2)]


    @lru_cache()
    def adjacent_trees(self, x, y):
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


    # def plot(self):
    #     colors = {'unburnt':'green',
    #               'burning':'red',
    #               'ember':'orange',
    #               'ash':'grey'}
 
    #     coords = [t.lat_lon for t in self.sampled_trees]
    #     x_y = [t.x_y for t in self.sampled_trees]

    #     color = [colors[t.state] for t in self.sampled_trees] 
    #     lat, lon, z = list(map(list, zip(*coords)))
    #     x, y, z = list(map(list, zip(*x_y))) 
        
    #     # plt.scatter(lat, lon, c=z, s=3, alpha=0.5)
    #     plt.scatter(lat, lon, c=color, s=3, alpha=0.5)
    #     # ax1 = plt.subplot(212) 
    #     # ax1.scatter(lat, lon, c=color, s=2, alpha=0.3)
        
    #     # ax2 = plt.subplot(221) 
    #     # ax2.scatter(lat, lon, c=z, s=2, alpha=0.3)
    #     # ax2.set_title('Lat Long')
    #     # plt.colorbar(ax2)
        
    #     # ax3 = plt.subplot(222) 
    #     # ax3.scatter(y, x, c=z, s=3, alpha=0.3)
    #     # ax3.set_title('Meters') 
    #     # # plt.colorbar(ax3)
 
    def plot(self, angle = 60): 
        colors = {'unburnt':'green',
                  'burning':'red',
                  'ember':'orange',
                  'ash':'grey'} 
        
        x_y = [t.lat_lon for t in self.sampled_trees]

        color = [colors[t.state] for t in self.sampled_trees]  
        x, y, z = list(map(list, zip(*x_y))) 

        x = np.array(x)#.reshape(self.terrain.num_points, self.terrain.num_points)
        y = np.array(y)#.reshape(self.terrain.num_points, self.terrain.num_points)
        z = np.array(z)#.reshape(self.terrain.num_points, self.terrain.num_points)
         
         
        ax = Axes3D(plt.figure(figsize=(15, 15)))
        ax.scatter(x, y, z, c=color, marker='^') 
        ax.view_init(35, angle)  
        plt.show() 
            
            
    def reset_forest(self, params):
        ''' aux method to replicate simulation '''
        self._forest_gen(params['tree_params'])

#%%

 