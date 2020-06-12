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
 
        self._gen_dimensions()
        self.points = self._gen_coordinates()



    def _gen_dimensions(self):
        x1, y1, _, _ = utm.from_latlon(self.shape[0][0], self.shape[0][1])  
        x2, y2, _, _ = utm.from_latlon(self.shape[1][0], self.shape[1][1])
        
        self.width = int(abs(x1 - x2))
        self.length = int(abs(y1 - y2))
        
        
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
        
            if iter % 3 == 0:
                time.sleep(0.5)
                if verbose: print(iter)
            iter += 1 
        return lat_lon_alt
 
    
    def _gen_coordinates(self):
        ''' 
        required for dimensioning the simulation
        '''    
        coordinates = list() # lat, long, z, x, y
        for point in self.lat_lon_alt:
            lat, lon, z = point
            x, y, _, _ = utm.from_latlon(lat, lon)
            coordinates.append((lat, lon, z, x, y))

        p0 = [p[0] for p in coordinates] # lat
        p1 = [p[1] for p in coordinates] # lon
        p2 = [float(p[2]) for p in coordinates] # z
        
        p3 = [p[3] for p in coordinates] # x
        p3 = [p - min(p3) for p in p3]
        
        p4 = [p[4] for p in coordinates] # y
        p4 = [p - min(p4) for p in p4]
        
        
        
        points = [(lat, lon, z, x, y) for lat in p0 for lon in p1 for z in p2 
               for x in p3 for z in p4]
        
        self.interpolated_lat_lon_alt = interpolate.interp2d(p0, p1, p2, kind='linear')
        self.interpolated_cartesian = interpolate.interp2d(p3, p4, p2, kind='linear')

        return points
 
    
    def _plot3d(self, n=20):
 
        x = [p[0] for p in self.lat_lon_alt]
        y = [p[1] for p in self.lat_lon_alt]
        z = [p[2] for p in self.lat_lon_alt]

        x = np.array(x).reshape(self.num_points, self.num_points)
        y = np.array(y).reshape(self.num_points, self.num_points)
        z = np.array(z).reshape(self.num_points, self.num_points)
         
        for angle in range(0, 360, n):
        # angle = 60
            ax = Axes3D(plt.figure())
            ax.plot_surface(x, y, z, cmap=plt.cm.viridis, cstride=1, rstride=1)
        
            ax.view_init(30, angle) 
            plt.show()
        # time.sleep(0.1)
    
#%%
 