
# import os

import matplotlib.pyplot as plt
from collections import Counter

from simul.forest import Forest
from simul.fire import Fire
from resources import tree_db as tb
from resources import soil_db as sb

tree_db = tb.tree_db
soil_db = sb.soil_db


params = dict()
params['forest_params'] = dict()
params['forest_params']['forest_mixture'] = 0.5
#Tree density in primary forests varies from 50,000-100,000 trees per square km
params['forest_params']['forest_density'] = 0.8 # 0.9 - 0.95
params['forest_params']['safe_radius'] = 16

params['terrain_params'] = dict()
params['terrain_params']['shape'] = [(r, c) for r in range(100) for c in range(100)]
params['terrain_params']['type'] = '2d'
params['terrain_params']['soil'] = 'grass'

params['tree_params'] = dict()
params['tree_params']['type'] = tree_db['pine']
params['tree_params']['fuel_perc'] = 100
params['tree_params']['ember'] = False
params['tree_params']['burning'] = False

params['fire_params'] = dict()
params['fire_params']['starting_tree_coords'] = (51, 10)
params['fire_params']['spread'] = 1


 
fire = Fire(params)
fire.start_fire()

while  len(fire.forest.tree_state['burning']) > 0 or (len(fire.forest.tree_state['burning'])==0 
                                                      and len(fire.forest.tree_state['ember']) > 0):
    fire.update_fire(verbose=True)
    
    state = [t.state for t in fire.forest.tree_lst]
    print(Counter(state))
    fire.forest.plot()
    plt.show()

 