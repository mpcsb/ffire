# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""
import math

class Weather():
    def __init__(self, timestamp):
        pass
        # self.weather = Weather()
        # self.humidity = Humidity()
        # self.timestamp = self.timestamp = timestamp
 

class Wind():
    def __init__(self, params):
        self.altitude = 10 # ability to create several layers, by altitude
        self.speed = params['weather_params']['speed']
        self.angle = params['weather_params']['degree']
    
    def update_wind(self, speed, angle):
        self.speed = speed
        self.angle = angle 
        
        
    def fire_projection(self, x, y, d):
        ''' 
        defines box of action of wind on burning tree, based on safe distance d
        A--------C
        |        |
        tree     F(ront)
        |        |
        B--------D
        '''
        A = (x + d * math.sin(self.angle), y + d * math.cos(self.angle))
        B = (x - d * math.sin(self.angle), y - d * math.cos(self.angle))
        F = (x + self.speed * math.sin(self.angle), y + self.speed * math.cos(self.angle))
        C = (F[0] + d * math.sin(self.angle), F[1] + d * math.cos(self.angle))
        D = (F[0] - d * math.sin(self.angle), F[1] - d * math.cos(self.angle))
        
        return A, B, C, D
    
    

class Humidity():
    def __init__(self):
        pass
    
    def update_humidity(self, rel_hum):
        self.relative_humidity = rel_hum
        # self.timestamp = timestamp
        
#%%
 