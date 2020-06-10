
import os
os.chdir(r'C:\Users\Miguel\Documents\repos\ffire\ffire')

import matplotlib.pyplot as plt
from collections import Counter
from pylab import rcParams
rcParams['figure.figsize'] = 15, 10

# from simul.forest import Forest
from simul.fire import Fire
from resources import tree_db as tb
from resources import soil_db as sb

tree_db = tb.tree_db
soil_db = sb.soil_db


params = dict()
params['forest_params'] = dict()
params['forest_params']['forest_mixture'] = 0.5
#Tree density in primary forests varies from 50,000-100,000 trees per square km
params['forest_params']['forest_density'] = 0.95 # 0.9 - 0.95
params['forest_params']['safe_radius'] = 6.0

params['terrain_params'] = dict()
# params['terrain_params']['shape'] = [(r, c) for r in range(1200) for c in range(1000)]
p2 = 38.721665, -9.434295
p1 = 38.727851, -9.425669
params['terrain_params']['shape'] = (p1, p2)
params['terrain_params']['num_points'] = 6

params['terrain_params']['soil'] = 'grass'

params['tree_params'] = dict()
params['tree_params']['type'] = tree_db['pine']
params['tree_params']['ember'] = False
params['tree_params']['burning'] = False

params['fire_params'] = dict()
params['fire_params']['starting_tree_coords'] = (200, 650, 0)
params['fire_params']['spread'] = 1



fire = Fire(params)
fire.start_fire()
print(f'Width:{fire.forest.terrain.width} Length:{fire.forest.terrain.length}')

# try:
#     fire.forest.terrain.plot3d()
# except ValueError:
#     pass

it = 0
while  len(fire.forest.tree_state['burning']) > 0 or (len(fire.forest.tree_state['burning'])==0
                                                      and len(fire.forest.tree_state['ember']) > 0):
    fire.update_fire(verbose=True)
    state = [t.state for t in fire.forest.tree_lst]
    print(Counter(state))

    if it % 10 == 0:
        fire.forest.plot()
        plt.show()

    it += 1
#%%
 