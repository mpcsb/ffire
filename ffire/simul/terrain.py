# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:37:58 2020

@author: z003njns
"""

class Terrain():
    def __init__(self, terrain_params):
        self.shape = terrain_params['shape'] # collection of points or GIS data
        self.type = terrain_params['type'] # 2d/3d

