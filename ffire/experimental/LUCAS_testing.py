# -*- coding: utf-8 -*-
"""
Created on Sun May 31 23:21:01 2020

@author: Miguel
"""

import os
os.chdir(r'C:\Users\Miguel\Documents\repos\ffire\ffire\data')

import pandas as pd

df = pd.read_csv('GRID_CSVEXP_20171113.csv')
 
df_pt = df[df['NUTS0_13']=='PT'] 
  
df_pt['ELEV'].hist(bins='auto')
X = df_pt['X_WGS84'].values
Y = df_pt['Y_WGS84'].values
Z = df_pt['ELEV'].values 

import matplotlib.pyplot as plt
plt.scatter(X,Y, c=Z,s=1)
#%%
