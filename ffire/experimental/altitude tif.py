# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 18:44:17 2020

@author: Miguel
"""

#%%


from osgeo import gdal
gdal.UseExceptions()

ds = gdal.Open(r'C:\WindNinja\WindNinja-3.5.3\1\11.tif')
band = ds.GetRasterBand(1)
elevation = band.ReadAsArray()

print(elevation.shape)
print(elevation)


import matplotlib.pyplot as plt
plt.imshow(elevation, cmap='gist_earth')
plt.show()