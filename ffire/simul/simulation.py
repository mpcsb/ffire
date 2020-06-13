from simul.fire import Fire
import matplotlib.pyplot as plt
from collections import Counter


class simulation_run():
    
    def __init__(self, params):
        
        self.fire = Fire(params)
        self.fire.start_fire()
        self.fire.forest.terrain.plot3d(60)
        print(f'Width:{self.fire.forest.terrain.width} Length:{self.fire.forest.terrain.length}')
 
        it = 0
        while len(self.fire.forest.tree_state['burning']) > 0 or\
            (len(self.fire.forest.tree_state['burning']) == 0 and len(self.fire.forest.tree_state['ember']) > 0):
                
            self.update_fire(verbose=True)
            state = [t.state for t in self.fire.forest.tree_lst]
            print(Counter(state))
        
            if it % 10 == 0:
                self.fire.forest.plot()
                plt.show()
            it += 1
  
    
    def _spread_fire(self):
        '''
        iterates all burning trees
        updates forest variables burning_trees list and safe_tree
        '''

        recent_burns = list()
        for tree in self.fire.forest.tree_state['burning']:
            try:
                adjacent_trees = set([t for (d, t) in self.fire.forest.neighbours[tree]])
            except KeyError:
                continue
            
            for t in adjacent_trees:
                if t.state == 'unburnt':
                    t.state = 'burning'
                    recent_burns.append(t)

        if len(recent_burns) > 0: # update state dict
            for t in recent_burns:
                if t in self.fire.forest.tree_state['unburnt']:
                    self.fire.forest.tree_state['burning'].add(t)
                    self.fire.forest.tree_state['unburnt'].remove(t)
            self.fire.forest.tree_state['burning_recent'] = list(adjacent_trees)
        else:
            self.fire.forest.tree_state['burning_recent'] = []


    def _eval_burning_trees(self):
        ''' determines tree transition from burning to ember '''

        for t in self.fire.forest.tree_state['burning'].copy():
            t.fuel_perc -= 2 # constant decrease in fuel [TODO] contextual
            if t.fuel_perc <= 10: # at this point it will turn to ember (?)
                if t.state == 'burning':
                    t.state = 'ember'
                    self.fire.forest.tree_state['ember'].add(t)
                    self.fire.forest.tree_state['burning'].remove(t)


    def _eval_embers(self):
        ''' determines tree transition from ember to charcoal'''

        for t in self.fire.forest.tree_state['ember'].copy():
            t.fuel_perc -= 0.3 # 1 % decrease each iteration
            if t.fuel_perc <= 0: # [TODO] makes this probabillistic
                t.state = 'ash'
                self.fire.forest.tree_state['ash'].add(t)
                self.fire.forest.tree_state['ember'].remove(t)


    def update_fire(self, verbose=False):
        self._spread_fire()
        self._eval_burning_trees()
        self._eval_embers()
 