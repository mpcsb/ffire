# -*- coding: utf-8 -*-
"""
Created on Fri May 29 21:31:43 2020

@author: Miguel
"""
from math import sqrt
def dist(p,q):
    return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


class Fire():
    def __init__(self, fire_params, Forest):
        self.forest = Forest
        distance_lst = [(dist(k, fire_params['starting_tree_coords']), k)
                        for k in self.forest.coord_dict]
        self.starting_tree_coords = min(distance_lst)[1] # tree coord closest to starting_tree_coords

        self.spread = fire_params['spread']



    def start_fire(self):
        ''' starts fire in one tree '''

        starting_tree = self.forest.coord_dict[self.starting_tree_coords]
        starting_tree.state = 'burning'

        self.forest.burning_trees.append(starting_tree)
        self.forest.safe_trees.remove(starting_tree)


    def _spread_fire(self, verbose=False):
        '''
        iterates all burning trees
        updates forest variables burning_trees list and safe_tree
        '''
        new_burning_trees = list()
        for tree in self.forest.burning_trees:

            if tree not in self.forest.neighbours.keys(): # not adjacent
                next
            else:
                adjacent_trees = [t for (d, t) in self.forest.neighbours[tree]]
                for t in adjacent_trees:
                    t.state = 'burning'
                new_burning_trees.extend(adjacent_trees)

        new_burning_trees = list(set(new_burning_trees))

        if len(new_burning_trees) > 0:
            self.forest.burning_trees = list(set(new_burning_trees).union(set(self.forest.burning_trees)))
            self.forest.safe_trees = [t for t in self.forest.safe_trees if t not in
                                 new_burning_trees]
        if verbose:
            print(f'Safe trees: {len(self.forest.safe_trees)}, Burning trees:{len(self.forest.burning_trees)}, Ember trees:{len(self.forest.ember_trees)}')


    def _adjust_fuel(self):
        ''' determines tree transition from burning to ember'''
        remove_lst = list()
        for t in self.forest.burning_trees:
            t.fuel_perc -= 5 # constant decrease in fuel [TODO] contextual
            if t.fuel_perc <= 0:
                remove_lst.append(t)
                t.state = 'ember'
                self.forest.ember_trees[t] = 0
        self.forest.burning_trees = [t for t in self.forest.burning_trees \
                                     if t not in remove_lst]


    def _consumed_trees(self):
        ''' determines tree transition from ember to charcoal'''
        burnt_list = list()
        for t in self.forest.ember_trees:
            self.forest.ember_trees[t] += 1
            if self.forest.ember_trees[t] > 10: # [TODO] makes this probabillistic
                t.state = 'charcoal'

                burnt_list.append(t)

        for t in burnt_list:
            del self.forest.ember_trees[t]

        self.forest.burnt_trees.extend(burnt_list)


    def update_fire(self, verbose=False):
        self._spread_fire(verbose)
        self._adjust_fuel()
        self._consumed_trees()