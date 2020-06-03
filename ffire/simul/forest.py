# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""
from math import sqrt
import matplotlib.pyplot as plt
import random
import copy
from functools import lru_cache

from simul.terrain import Terrain
from simul.tree import Tree


def dist(p,q):
    return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


class Forest:

    def __init__(self, params):
        self.forest_density = params['forest_params']['forest_density']
        self.forest_mixture = params['forest_params']['forest_mixture']
        self.terrain = Terrain(params['terrain_params'])
        self.safe_radius = params['forest_params']['safe_radius']

        self._forest_gen(params['tree_params'])
        self._quadrant_gen()
        self._nearest_trees()
        self._coord2tree()

        self.safe_trees = copy.deepcopy(self.tree_lst)
        self.burning_trees = list()
        self.ember_trees = dict()
        self.burnt_trees = list()


    def _forest_gen(self, tree_params):
        ''' generate collection of trees over the terrain '''
        self.tree_lst = list()
        for coord in self.terrain.shape:
            if random.random() > self.forest_density:
                self.tree_lst.append(Tree(tree_params, coord))


    def _quadrant_gen(self):
        width, length = max(self.terrain.shape)

        d = self.safe_radius
        self.quadrants = {x: {y: list() for y in range((length + 1) // d + 1)}
                          for x in range((width + 1) // d + 1)}

        for t in self.tree_lst:
            x, y = t.coord
            self.quadrants[x // d][y // d].append(t)


    # def _nearest_trees(self):
    #     ''' generates a dictionary with the nearest trees up to a distance '''
    #     self.neighbours = dict()
    #     for p in self.tree_lst:
    #         for q in self.tree_lst:
    #             d = dist(p.coord, q.coord)
    #             if 0.0 < d < p.safe_radius:
    #                 if p in self.neighbours.keys():
    #                     self.neighbours[p].append((d, q))
    #                 else:
    #                     self.neighbours[p] = [(d, q)]
    def _nearest_trees(self):
        ''' generates a dictionary with the nearest trees up to a distance '''
        self.neighbours = dict()
        for t1 in self.tree_lst:
            x, y = t1.coord
            x = x // self.safe_radius
            y = y // self.safe_radius

            comparable_trees = self.__adjacent_trees(x, y)
            # print(len(comparable_trees))
            for t2 in comparable_trees:
                d = dist(t1.coord, t2.coord)
                if 0.0 < d < self.safe_radius:
                    if t1 in self.neighbours.keys():
                        self.neighbours[t1].append((d, t2))
                    else:
                        self.neighbours[t1] = [(d, t2)]


    @lru_cache()
    def __adjacent_trees(self, x, y):
        comparable_trees = list()
        diffs = [(dx, dy) for dx in range(-2, 2) for dy in range(-2, 2)]

        for delta in diffs:
            dx, dy = delta
            # print(x, y)
            try:
                t_lst = self.quadrants[x + dx][y + dy]
                comparable_trees.extend(t_lst)
            except KeyError:
                next

        return comparable_trees


    def _coord2tree(self):
        ''' mapping from coordinate to tree '''
        self.coord_dict = dict()
        for t in self.tree_lst:
            self.coord_dict[t.coord] = t

    def tree_feature_distribution(self, feature):
        height_distribution = [t.feature for t in self.tree_lst]
        plt.hist(height_distribution, bins='auto')

    def plot(self):
        colors = {'unburnt' :'green', 'burning':'red', 'ember':'orange', 'charcoal':'black'}

        coords = [t.coord for t in self.tree_lst]
        color = [colors[t.state] for t in self.tree_lst]
        x, y = list(map(list, zip(*coords)))
        plt.scatter(x, y, c=color, s=2)





