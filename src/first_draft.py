# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""

import numpy as np
import matplotlib.pyplot as plt
# plt.plot([1, 2, 3, 4])

class Terrain():
    def __init__(self, kwargs):
        self.shape = kwargs['shape'] # collection of points or GIS data
        self.type = kwargs['type'] # 2d/3d


class Tree():
    def __init__(self, params, coord):
        h = params['type']['height']
        self.height = np.random.normal(h, h * 0.2)
        self.type = params['type'] # dict containing properties of tree:
                                   # species name, radius, burn ability, ...
        self.fuel_perc = params['fuel_perc'] # how burnt the tree is
        self.ember = params['ember']
        self.coord = coord

    # def _sample_height(h=11):
    #     # http://blogs.oregonstate.edu/geog566spatialstatistics/2019/04/19/point-pattern-analysis-of-tree-distribution-by-height-in-the-hj-andrews-forest/
    #     return np.random.normal(h, h * 0.2)


class Forest():
    def __init__(self, terrain_params, tree_params):
        self.terrain = Terrain(terrain_params)
        self.tree_lst = list()
        self.forest = self._forest_gen(tree_params)

    def _forest_gen(self, tree_params):
        for coord in self.terrain.shape:
            self.tree_lst.append(Tree(tree_params, coord))

    def plot(self):
        height_distribution = [t.height for t in self.tree_lst]
        plt.hist(height_distribution, bins='auto')

class Weather():
    def __init__(self, kwargs):
        self.rain = kwargs['rain']
        self.rel_humidity = kwargs['rel_humidity']
        self.wind = kwargs['wind']


class Fire():
    def __init__(self, kwargs):
        self.spread = kwargs['spread']



class Simulation(Forest, Weather, Fire):
    def __init__(self, args):
        self.args = args


#%% example run

tree_db = dict()
tree_db['pine'] = {'species': 'pine', 'height': 11.8, 'dist30':12.5, 'dist30_sd':4.4, 'dist1':2.1, 'dist1_sd':2}

params = dict()
params['terrain_params'] = dict()
params['terrain_params']['shape'] = [(r, c) for r in range(1000) for c in range(1000)]
params['terrain_params']['type'] = '2d'

params['tree_params'] = dict()
params['tree_params']['type'] = tree_db['pine']
params['tree_params']['fuel_perc'] = 100
params['tree_params']['ember'] = False


f = Forest(params['terrain_params'], params['tree_params'])

f.plot()
