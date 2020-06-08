
import numpy as np
import requests
import time
def url(lat, long):
    url = f'https://elevation.racemap.com/api?lat={lat}&lng={long}'
    return url.format(lat, long)

38.730494, -9.468652
38.740106, -9.465151

np_lat = np.linspace(38.740106, 38.730494, num=30, endpoint=True)
np_long = np.linspace(-9.468652, -9.465151, num=30, endpoint=True)


iter = 0
xyz = list()
for p in [(lat, long) for lat in list(np_lat) for long in list(np_long)]:
    r = requests.get(url(p[0],p[1]))
    while '<html>' in r.text :
        time.sleep(1)
        r = requests.get(url(p[0],p[1]))

    point = (p[0],p[1],  r.text )
    xyz.append(point)
    print(r.text)

    if iter %3 == 0:
        time.sleep(0.5)
        print(iter)


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
x = np.array(x).reshape(30,30)
y = np.array(y).reshape(30,30)
z = np.array(z).reshape(30,30)

from mpl_toolkits.mplot3d import Axes3D

for angle in range(0, 360, 20):
    ax = Axes3D(plt.figure())
    ax.plot_surface(x, y, z, cmap=plt.cm.viridis, cstride=1, rstride=1)

    ax.view_init(30, angle)
    plt.draw()
    plt.show()
    time.sleep(0.1)
    # plt.pause(.001)