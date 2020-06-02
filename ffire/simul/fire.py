# -*- coding: utf-8 -*-
"""
Created on Fri May 29 21:31:43 2020

@author: Miguel
"""

class Fire():
    def __init__(self, fire_params):
        self.starting_tree_coords = fire_params['starting_tree_coords']
        self.spread = fire_params['spread']
        
        
    def start_fire(self, forest):
        ''' starts fire in one tree '''
        startint_tree = forest.coord_dict[self.starting_tree_coords]
        forest.burning_trees.append(startint_tree)
        forest.safe_trees.remove(startint_tree)
    
    
    def spread_fire(self, forest):
        ''' 
        iterates all burning trees
        updates forest variables burning_trees list and safe_tree
        '''
        new_burning_trees = list()
        for tree in forest.burning_trees:
            adjacent_trees = [t for d, t in forest.neighbours[tree]] 
            new_burning_trees.extend(adjacent_trees)
        
        new_burning_trees = list(set(new_burning_trees))
        if len(new_burning_trees) > 0:
            forest.burning_trees = list(set(new_burning_trees).union(set(forest.burning_trees)))
            forest.safe_trees = [tree for tree in forest.safe_trees if tree not in
                                 new_burning_trees]
        print(f'Safe trees: {len(forest.safe_trees)}, Burning trees:{len(forest.burning_trees)}')


 