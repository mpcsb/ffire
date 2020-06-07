 
from math import sqrt 
from simul.forest import Forest


def dist(p,q):
    return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


class Fire():
    def __init__(self, params):
        
        self.forest = Forest(params)
        # distance of all trees to starting tree. 
        # if the coordinates for the starting tree are not found in the forrest
        # then the closest is chosen.
        distance_lst = [(dist(k, params['fire_params']['starting_tree_coords']), k)
                        for k in self.forest.coord_dict]
        self.starting_tree_coords = min(distance_lst)[1]  
         

    def start_fire(self):
        ''' starts fire in one tree '''

        starting_tree = self.forest.coord_dict[self.starting_tree_coords]
        starting_tree.state = 'burning'
        
        self.forest.tree_state['burning'].add(starting_tree)
        self.forest.tree_state['unburnt'].remove(starting_tree) 
        
        print(starting_tree.coord)
 
        # self.forest.tree_state['recent_burn'].add(starting_tree)


    def _spread_fire(self):
        '''
        iterates all burning trees
        updates forest variables burning_trees list and safe_tree
        '''
        
        recent_burns = list()
        for tree in self.forest.tree_state['burning']: 
             
            adjacent_trees = set([t for (d, t) in self.forest.neighbours[tree]])
             
            for t in adjacent_trees:
                if t.state == 'unburnt':
                    t.state = 'burning'
                    recent_burns.append(t)
            
        if len(recent_burns) > 0: # update state dict
            for t in recent_burns:
                if t in self.forest.tree_state['unburnt']:
                    self.forest.tree_state['burning'].add(t)
                    self.forest.tree_state['unburnt'].remove(t)
            self.forest.tree_state['burning_recent'] = list(adjacent_trees)
        else:
            self.forest.tree_state['burning_recent'] = []
  


    def _eval_burning_trees(self):
        ''' determines tree transition from burning to ember '''
         
        for t in self.forest.tree_state['burning'].copy():
            t.fuel_perc -= 5 # constant decrease in fuel [TODO] contextual
            if t.fuel_perc <= 10: # at this point it will turn to ember (?) 
                if t.state == 'burning':
                    t.state = 'ember'
                    self.forest.tree_state['ember'].add(t) 
                    self.forest.tree_state['burning'].remove(t)  


    def _eval_embers(self):
        ''' determines tree transition from ember to charcoal'''
         
        for t in self.forest.tree_state['ember'].copy(): 
            t.fuel_perc -= 1 # 1 % decrease each iteration
            if t.fuel_perc < 1: # [TODO] makes this probabillistic
                t.state = 'ash' 
                self.forest.tree_state['ash'].add(t) 
                self.forest.tree_state['ember'].remove(t)
 
  
    def update_fire(self, verbose=False):
        self._spread_fire()
        self._eval_burning_trees()
        self._eval_embers()
        # if verbose:
        #     print(f'Safe: {len(self.forest.safe_trees)}, Burning:{len(self.forest.burning_trees)}, Ember:{len(self.forest.ember_trees)}, Burnt:{len(self.forest.burnt_trees)}')
