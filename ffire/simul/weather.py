# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""


class Weather():
    def __init__(self, timestamp):
        pass
        # self.weather = Weather()
        # self.humidity = Humidity()
        # self.timestamp = self.timestamp = timestamp
 

class Wind():
    def __init__(self, altitude=10):
        self.altitude = altitude # ability to create several layers, by altitude
    
    def update_wind(self, speed, direction):
        self.wind_speed = speed
        self.wind_direction = direction 


class Humidity():
    def __init__(self):
        pass
    
    def update_humidity(self, rel_hum):
        self.relative_humidity = rel_hum
        # self.timestamp = timestamp
        
#%%
import math

def coords_to_north(p1, p2):
    lat1, lon1 = p1
    lat2, lon2 = p2
    
    lat1 = lat1 * math.pi / 180;
    lat2 = lat2 * math.pi / 180;
    dLon = (lon2-lon1) * math.pi / 180;
    y = math.sin(dLon) * math.cos(lat2);
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2)  *math.cos(dLon);

    bearing = math.atan2(y, x) * 180 / math.pi;
    if bearing < 0:
        bearing = bearing + 360;

    return bearing


p2 = 38.720665, -9.430295
p1 = 38.730851, -9.420669

coords_to_north(p1, p2)