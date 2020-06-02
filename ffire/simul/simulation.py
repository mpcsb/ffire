 
import os
os.chdir(r'C:\Users\Miguel\Documents\repos\ffire\ffire')

from simul.forest import Forest
from simul.fire import Fire
from resources import tree_db as tb 
from resources import soil_db as sb

tree_db = tb.tree_db
soil_db = sb.soil_db


params = dict()

params['forest_params'] = dict()
params['forest_params']['forest_mixture'] = 0.5
params['forest_params']['forest_density'] = 0.3

params['terrain_params'] = dict()
params['terrain_params']['shape'] = [(r, c) for r in range(50) for c in range(50)]
params['terrain_params']['type'] = '2d'
params['terrain_params']['soil'] = 'weed'

params['tree_params'] = dict()
params['tree_params']['type'] = tree_db['pine']
params['tree_params']['fuel_perc'] = 100
params['tree_params']['ember'] = False
params['tree_params']['burning'] = False
params['tree_params']['safe_radius'] = 6.0

params['fire_params'] = dict()
params['fire_params']['starting_tree_coords'] = (1,1)
params['fire_params']['spread'] = 1

f = Forest(params) 
f.neighbours
 

fire = Fire(params['fire_params'])
  
fire.start_fire(f)
 
 

for _ in range(25):
    
    fire.spread_fire(f)

#%%
