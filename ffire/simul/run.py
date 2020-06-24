
import os
os.chdir(r'C:\Users\Miguel\Documents\repos\ffire\ffire')

# import matplotlib.pyplot as plt
# from collections import Counter
from pylab import rcParams
rcParams['figure.figsize'] = 15, 15

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
p1 = 38.738802, -9.332599
p2 = 38.790060, -9.390210
params['terrain_params']['shape'] = (p1, p2)
params['terrain_params']['num_points'] = 100

params['terrain_params']['soil'] = 'grass'

params['tree_params'] = dict()
params['tree_params']['type'] = tree_db['pine']
 
params['fire_params'] = dict()
params['fire_params']['starting_tree_coords'] = (160, 160, 0)
  
params['weather_params'] = dict()
params['weather_params']['degree'] = 90
params['weather_params']['speed'] = 0

 
s = simulation_run(params)

#%%
 