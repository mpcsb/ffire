# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""
import numpy as np
import requests
import time
import utm
from scipy import interpolate
# import tqdm 
 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Terrain():
    
    def __init__(self, terrain_params):
        self.shape = terrain_params['shape'] # collection of points or GIS data
        self.num_points = terrain_params['num_points'] 

        self.lat_lon_alt = self._sample_altitude(self.shape[0], self.shape[1], self.num_points)
        self._plot3d()
        
        x1, y1, _, _ = utm.from_latlon(self.shape[0][0], self.shape[0][1])  
        x2, y2, _, _ = utm.from_latlon(self.shape[1][0], self.shape[1][1])
        
        self.width = int(abs(x1 - x2))
        self.length = int(abs(y1 - y2))
        
        self.points = self._cartesian_coords()
 

    def _sample_altitude(self, p1, p2, n_points = 20, verbose=True): 
        
        def url(lat, long):
            url = f'https://elevation.racemap.com/api?lat={lat}&lng={long}'
            return url.format(lat, long)
        
        np_lat = np.linspace(p1[0], p2[0], num=n_points, endpoint=True)
        np_long = np.linspace(p1[1], p2[1], num=n_points, endpoint=True)
         
        iter = 0
        lat_lon_alt = list()
        for p in [(lat, long) for lat in list(np_lat) for long in list(np_long)]:
            r = requests.get(url(p[0],p[1]))
            while '<html>' in r.text :
                time.sleep(1)
                r = requests.get(url(p[0],p[1]))
        
            point = (p[0], p[1], float(r.text))
            lat_lon_alt.append(point) 
        
            if iter %3 == 0:
                time.sleep(0.5)
                if verbose: print(iter)
            iter += 1 
        return lat_lon_alt


    def _cartesian_coords(self):
        ''' converts lat,lon to cartesian coordinates. 
            required for dimensioning the simulation
        '''    
        cartesian_points = list() 
        for point in self.lat_lon_alt:
            lat, long, z = point
            x, y, _, _ = utm.from_latlon(lat, long)
            cartesian_points.append((x, y, z))
    
        p0 = [p[0] for p in cartesian_points] # x
        p0 = [p - min(p0) for p in p0]
        
        p1 = [p[1] for p in cartesian_points] # y
        p1 = [p - min(p1) for p in p1]
        
        p2 = [float(p[2]) for p in cartesian_points] # z
        
        xyz = [(x,y,z) for x in p0 for y in p1 for z in p2]
    
        self.interpolated_f = interpolate.interp2d(p0, p1, p2, kind='linear')

        return xyz
 
    
    def _plot3d(self):
        xyz = self.lat_lon_alt
        x = [p[0] for p in xyz]
        y = [p[1] for p in xyz]
        z = [p[2] for p in xyz]
         
        x = np.array(x).reshape(self.num_points, self.num_points)
        y = np.array(y).reshape(self.num_points, self.num_points)
        z = np.array(z).reshape(self.num_points, self.num_points)
         
        for angle in range(0, 360, 20):
        # angle = 60
            ax = Axes3D(plt.figure())
            ax.plot_surface(x, y, z, cmap=plt.cm.viridis, cstride=1, rstride=1)
        
            ax.view_init(30, angle) 
            plt.show()
        # time.sleep(0.1)
    
#%%
 