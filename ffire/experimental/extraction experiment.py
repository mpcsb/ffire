
import numpy as np
import requests
import time
def url(lat, long):
    url = f'https://elevation.racemap.com/api?lat={lat}&lng={long}'
    return url.format(lat, long)



np_lat = np.linspace(38.731449, 38.737212, num=10, endpoint=True)
np_long = np.linspace(-9.474691, -9.466750, num=10, endpoint=True)


iter = 0
xyz = list()
for p in [(lat, long) for lat in list(np_lat) for long in list(np_long)]:
    r = requests.get(url(p[0],p[1]))
    while '<html>' in r.text :
        time.sleep(0.5)
        r = requests.get(url(p[0],p[1]))

    point = (p[0],p[1],  r.text )
    xyz.append(point)
    print(r.text)


#%%

x = [p[0] for p in xyz]
y = [p[1] for p in xyz]
z = [float(p[2]) for p in xyz]

import matplotlib.pyplot as plt

plt.scatter(x,y, c=z, alpha=0.7, s=93)
#%%

import numpy as np
import matplotlib.pyplot as plt


xx, yy = np.meshgrid(x, y)
_, zz = np.meshgrid(x, z)
# z = xx*0+yy*0+ np.random.random(size=[900,900])

from mpl_toolkits.mplot3d import Axes3D
ax = Axes3D(plt.figure())

ax.plot_surface(xx, yy, zz, cmap=plt.cm.viridis, cstride=1, rstride=1)
plt.show()