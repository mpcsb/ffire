from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
 
import numpy as np
import requests
import time
import utm

def url(lat, long):
    url = f'https://elevation.racemap.com/api?lat={lat}&lng={long}'
    return url.format(lat, long)

p2 = 38.685093, -9.309931
p1 = 38.693609, -9.301329

 
def sample_altitude(p1, p2, n_points = 5, verbose=False):
    
    np_lat = np.linspace(p1[0], p2[0], num=n_points, endpoint=True)
    np_long = np.linspace(p1[1], p2[1], num=n_points, endpoint=True)
    
    
    iter = 0
    xyz = list()
    for p in [(lat, long) for lat in list(np_lat) for long in list(np_long)]:
        r = requests.get(url(p[0],p[1]))
        while '<html>' in r.text :
            time.sleep(1)
            r = requests.get(url(p[0],p[1]))
    
        point = (p[0], p[1], r.text)
        xyz.append(point) 
    
        if iter %3 == 0:
            time.sleep(0.5)
            if verbose: print(iter)
        iter += 1
    return xyz

#%%

def plot(xyz):
    x = [p[0] for p in xyz]
    y = [p[1] for p in xyz]
    z = [p[2] for p in xyz]
     
    x = np.array(x).reshape(n_points, n_points)
    y = np.array(y).reshape(n_points, n_points)
    z = np.array(z).reshape(n_points, n_points)
    
    
    
    for angle in range(0, 360, 20):
        ax = Axes3D(plt.figure())
        ax.plot_surface(x, y, z, cmap=plt.cm.viridis, cstride=1, rstride=1)
    
        ax.view_init(30, angle)
        plt.draw()
        plt.show()
        time.sleep(0.1)

#%%

xyz = sample_altitude(p1, p2, n_points = 5, verbose=False)

cartesian_coords = list() 
for point in xyz:
    lat, long, z = point
    x, y, _, _ = utm.from_latlon(lat, long)
    cartesian_coords.append((x,y,z))


p0 = [p[0] for p in cartesian_coords]
p0 = [p - min(p0) for p in p0]
p1 = [p[1] for p in cartesian_coords]
p1 = [p - min(p1) for p in p1]
p2 = [p[2] for p in cartesian_coords]
xyz__ = [(x,y,z) for x in p0 for y in p1 for z in p2]

#%%
 
x = np.array(x).reshape(interpolating_points,interpolating_points)
y = np.array(y).reshape(interpolating_points,interpolating_points)
z = np.array(z).reshape(interpolating_points,interpolating_points)

for angle in range(0, 360, 20):
    ax = Axes3D(plt.figure())
    ax.plot_surface(x, y, z, cmap=plt.cm.viridis, cstride=1, rstride=1)

    ax.view_init(30, angle)
    plt.draw()
    plt.show()
    time.sleep(0.1)
 
#%%

 c = [(r, c) for r in range(1200) for c in range(1000)]