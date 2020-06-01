# -*- coding: utf-8 -*-
"""
Created on Sun May 31 00:16:25 2020

@author: Miguel
"""


import urllib.request
import json
 
API='AIzaSyB4lAc5DN-O6rAEN2RlQg7iDdzkZZfqBck'
url = 'https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key=' + API


 

response = urllib.request.urlopen(url)

data = json.loads(response.read())
print(data)
 
#%%


 
 