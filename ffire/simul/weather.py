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
    
    def update_wind(self, speed, angle):
        self.speed = speed
        self.angle = angle 


class Humidity():
    def __init__(self):
        pass
    
    def update_humidity(self, rel_hum):
        self.relative_humidity = rel_hum
        # self.timestamp = timestamp
        
#%%
 