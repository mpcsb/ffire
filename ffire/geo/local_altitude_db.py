# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 21:36:34 2020

@author: Miguel
"""

#%%
import os
from gmalthgtparser import HgtParser   
import gzip, shutil
os.chdir(r'C:\Users\Miguel\Documents\repos\ffire\elevation_data')
import random 
import io
from math import floor

import numpy as np
p1 = 38.798802, -9.332599
p2 = 38.790060, -9.350210 

np_lat = np.linspace(p1[0], p2[0], num=10, endpoint=True)
np_long = np.linspace(p1[1], p2[1], num=10, endpoint=True)
coords_lat_lon = [(lat, long) for lat in list(np_lat) for long in list(np_long)]

# tile_corners = [(35.16, 12.71),(35.77, 12.98)]

lat = floor(p1[0])
lon = floor(p1[1])

def filename_gen(lat, long):
    if lat >= 0: 
        fname = 'N'
        if lat >= 10:
            fname += str(lat)
        else:
            fname += '0' + str(lat)
    else:
        fname = 'S'
        if abs(lat) >= 10:
            fname += str(lat)
        else:
            fname += '0' + str(lat)
            
    if lon > 0:
        fname += 'E'
        if lon >= 100:
            fname +=str(lon)
        elif lon >= 10:
            fname += '0' + str(lon)
        else:
            fname += '00' + str(lon)
    else:
        fname += 'W'
        if abs(lon) >= 100:
            fname += str(abs(lon))
        elif abs(lon) >= 10:
            fname += '0' + str(abs(lon))
        else:
            fname += '00' + str(abs(lon))
    fname += '.hgt.gz'
    return  fname

filename = filename_gen(lat, lon)
path = filename[:3] + '/' + filename
decompressed_file = filename.replace('.gz', '')

 
content = gzip.open(path).read()
 
f = open(decompressed_file, 'wb')
f.write(content)
f.close()


 
#%%

with HgtParser(decompressed_file) as parser:
    for coord in coords_lat_lon:   
        lat_, lon_ = coord 
        alt = parser.get_elevation((lat_, lon_))
        print(lat_, lon_, alt[2])
os.remove(decompressed_file)

