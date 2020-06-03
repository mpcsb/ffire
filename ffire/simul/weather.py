# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""


class Weather():
    def __init__(self, params):
        self.rain = params['rain']
        self.relative_humidity = params['relative_humidity']
        self.wind_intensity = params['wind_intensity']
        self.wind_direction = params['wind_direction']
        self.timestamp = params['timestamp']

    def log(self):
        pass


class Wind():
    def __init__(self):
        pass
