
import os
os.chdir(r'C:\Users\Miguel\Documents\repos\ffire\ffire')

# import matplotlib.pyplot as plt
# from collections import Counter
from pylab import rcParams
rcParams['figure.figsize'] = 10, 15

from simul.simulation import simulation_run
from resources import tree_db as tb
from resources import soil_db as sb

tree_db = tb.tree_db
soil_db = sb.soil_db


params = dict()
params['forest_params'] = dict()
params['forest_params']['forest_mixture'] = 0.5
#Tree density in primary forests varies from 50,000-100,000 trees per square km
params['forest_params']['forest_density'] = 0.95 # 0.9 - 0.95
params['forest_params']['safe_radius'] = 6.0 # https://www.tandfonline.com/doi/full/10.1080/21580103.2016.1144541

params['terrain_params'] = dict()
# params['terrain_params']['shape'] = [(r, c) for r in range(1200) for c in range(1000)]
# p1 = 38.706934, -9.316414
p1 = 38.739934, -9.333414
p2 = 38.753648, -9.317820
params['terrain_params']['shape'] = (p1, p2)
params['terrain_params']['num_points'] = 8

params['terrain_params']['soil'] = 'grass'

params['tree_params'] = dict()
params['tree_params']['type'] = tree_db['pine']


params['fire_params'] = dict()
params['fire_params']['starting_tree_coords'] = (600, 640, 0)
 

params['weather_params'] = dict()
params['weather_params']['degree'] = 35
params['weather_params']['speed'] = 10


s = simulation_run(params)

#%%

for t in s.fire.forest.tree_lst:
    print(t.x_y[2], t.lat_lon[2])
    