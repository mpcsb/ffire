# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 22:21:08 2020

@author: Miguel
"""

>>> import overpy
>>> api = overpy.Overpass()
>>> result = api.query("node(50.745,7.17,50.75,7.18);out;")
>>> len(result.nodes)
1984
>>> len(result.ways)
0
>>> len(result.relations)
0
>>> node = result.nodes[2]
>>> node.id
100792806
>>> node.tags
{}


#%%

import overpy.helper

# 3600062594 is the OSM id of Chemnitz and is the bounding box for the request
street = overpy.helper.get_street(
    "Straße der Nationen",
    "3600062594"
)

street.ways

#%%
# p1 = 38.798802, -9.332599
# p2 = 38.790060, -9.350210
import overpy
import matplotlib.pyplot as plt
api = overpy.Overpass()

 

result = api.query("""
    way(38.685157, -9.480773, 38.787521, -9.460379) ["highway"];
    (._;>;);
    out body;
    """)
    
street_lst = list()
for way in result.ways:
    print("Name: %s" % way.tags.get("name", "n/a"))
    print("  Highway: %s" % way.tags.get("highway", "n/a"))
    print("  Nodes:")
    for node in way.nodes:
        street_lst.append((float(node.lat), float(node.lon)))
        
#%%
x = [p[0] for p in street_lst]
y = [p[1] for p in street_lst]



plt.scatter(x,y,s=1)