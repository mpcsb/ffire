# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""
from math import sqrt
import matplotlib.pyplot as plt
import random
# import copy
from functools import lru_cache

from simul.terrain import Terrain
from simul.tree import Tree


def dist(p,q):
    '''
    p = (1, 2, 3)
    q = (3, 4, 5)

    >>> dist(p,q)
    2.8284271247461903
    >>> dist(q,p)
    3.4641016151377544
    '''
    if len(p) == 2:
        return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
    if len(p) == 3:
        _, _, p3 = p
        _, _, q3 = q

        if p3 - q3 < 0:
            p_2d = (p[0], p[1])
            q_2d = (q[0], q[1])
            return dist(p_2d, q_2d)
        if p3 - q3 > 0: # burning tree is above other trees
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

        self.tree_state = {'unburnt': set(self.tree_lst),
                           'burning':set(),
                           'burning_recent':set(),
                           'ember':set(),
                           'ash':set()
                           }


    def _forest_gen(self, tree_params):
        ''' generate collection of trees over the terrain '''
        self.tree_lst = list()
        for coord in self.terrain.shape:
            if random.random() > self.forest_density:
                self.tree_lst.append(Tree(tree_params, coord))
        print(f'{len(self.tree_lst)} in forest')


    def _quadrant_gen(self):
        width, length = max(self.terrain.shape)

        d = self.safe_radius
        self.quadrants = {x: {y: list() for y in range((length + 1) // d + 1)}
                          for x in range((width + 1) // d + 1)}

        for t in self.tree_lst:
            x, y = t.coord
            self.quadrants[x // d][y // d].append(t)


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
        colors = {'unburnt':'green',
                  'burning':'red',
                  'ember':'orange',
                  'ash':'black'}
        def size_tree(h):
            if h>12:
                return 2
            else:
                return 1

        coords = [t.coord for t in self.tree_lst]
        color = [colors[t.state] for t in self.tree_lst]
        size = [size_tree(t.height) for t in self.tree_lst]
        x, y = list(map(list, zip(*coords)))
        plt.scatter(x, y, c=color, s=size, alpha=0.3)





