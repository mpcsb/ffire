 #%%
lat1, lon1 = 38.6891376,-9.3118181
lat2, lon2 = 38.691671, -9.305676 
url = 'https://elevation.racemap.com/api?lat={lat}&lng={long}'

u=url.format(lat=lat1, long=lon1)
  
    

#%%

import requests 
data = requests.get(u)  

print(data.text)

 