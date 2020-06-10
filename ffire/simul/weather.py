# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""


class Weather():
    def __init__(self, timestamp):
        self.weather = Weather()
        self.humidity = Humidity()
        self.timestamp = self.timestamp = timestamp
 

class Wind():
    def __init__(self):
        pass
    
    def update_wind(self, intensity, direction, timestamp):
        self.wind_intensity = intensity
        self.wind_direction = direction
        self.timestamp = timestamp


class Humidity():
    def __init__(self):
        pass
    
    def update_humidity(self, rel_hum, timestamp):
        self.relative_humidity = rel_hum
        self.timestamp = timestamp