# -*- coding: utf-8 -*-
"""
Created on Fri May 29 21:31:55 2020

@author: Miguel
"""
#%%
# import time
import os
os.chdir(r'C:\Users\Miguel\Documents\repos\ffire\ffire')

from simul.forest import Forest
from resources import tree_db as tb 
from resources import soil_db as sb

tree_db = tb.tree_db
soil_db = sb.soil_db

params = dict()

params['forest_params'] = dict()
params['forest_params']['forest_mixture'] = 0.5
params['forest_params']['forest_density'] = 0.3

params['terrain_params'] = dict()
params['terrain_params']['shape'] = [(r, c) for r in range(50) for c in range(1000)]
params['terrain_params']['type'] = '2d'
params['terrain_params']['soil'] = 'weed'

params['tree_params'] = dict()
params['tree_params']['type'] = tree_db['pine']
params['tree_params']['fuel_perc'] = 100
params['tree_params']['ember'] = False
 

f = Forest(params)

f.plot()
 
 