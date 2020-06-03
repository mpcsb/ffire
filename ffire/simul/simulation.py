
# import os

import matplotlib.pyplot as plt

from simul.forest import Forest
from simul.fire import Fire
from resources import tree_db as tb
from resources import soil_db as sb

tree_db = tb.tree_db
soil_db = sb.soil_db


params = dict()

params['forest_params'] = dict()
params['forest_params']['forest_mixture'] = 0.5
params['forest_params']['forest_density'] = 0.9

params['terrain_params'] = dict()
params['terrain_params']['shape'] = [(r, c) for r in range(250) for c in range(250)]
params['terrain_params']['type'] = '2d'
params['terrain_params']['soil'] = 'grass'

params['tree_params'] = dict()
params['tree_params']['type'] = tree_db['pine']
params['tree_params']['fuel_perc'] = 100
params['tree_params']['ember'] = False
params['tree_params']['burning'] = False
params['tree_params']['safe_radius'] = 6

params['fire_params'] = dict()
params['fire_params']['starting_tree_coords'] = (21,20)
params['fire_params']['spread'] = 1


#%%
f = Forest(params)

fire = Fire(params['fire_params'], f)
fire.start_fire( )

# l = len(f.safe_trees)

# while len(f.burning_trees) != l and len(f.burning_trees) > 0 and len(f.ember_trees) > 0:
for _ in range(1000):
    fire.update_fire(verbose=False)
    f.plot()
    plt.show()


#%%
