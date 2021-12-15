# H2O Olympics | Wildfire Challenge Submission

## Forest fire (ffire) simulation to assess wildfire risk

This submission is the implementation of an idea that focus around simulating fire dynamics (a complex process that is of course too ambitious for a project of this duration).  
The main ideas behind the data generating process is to utilize geometrical properties of the terrain and simulate the behavior of other factors in wind propagation (e.g. wind).  
The purpose of this tool is to assess risk in order to minimize real estate activity in areas where firefighting should be particularly hard. This can be assessed by analyzing the simulations and looking at the rate of burning trees per iteration, for instance.  

### Output  
This application currently generates 3d animations of fire propagation. This plot also displays historical wildfire perimeters extracted from https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-current-wildland-fire-perimeters. At this point it display one specific wildfire, but it can be adjusted easily, with the wildfire index & associated terrain specification.  
It also displays plots with the variation of several states of our simulated objects(burning trees, unburnt trees, ember, ash)
This objects can be used later on to quantify some indicators of risk of wildfire.  

## Input & simulation mechanics
This application requires a parameter dictionary that will be used in roughly the following order:  
1. Two points that define a rectangle where the simulation will be performed.
2. The number of points that are goint to access an altitude API, thus generating a 3d terrain. For instance if we set this parameter to 10, we are going to sample 10 equidistant points between our all latitudes and longitudes, thus having 100 altitude points.  
3. We then define the density of the forest that is going to populate this terrain. This will afterwards be used to randomly generating individual tree objects.
4. We have several parameters associated with fire propagation, namely minimum from a flame at which a tree will burn; and fire starting point.  
5. Wind direction and speed. This will impact the fire propagation, essentially generating a flame extension in the direction of the wind and proportional to the wind speed.  
6. With each iteration, trees will start to burn and will continue to propagate fire to their adjacent trees (all those that fall in the range of flammability define in the parameters).  

## Future features and caveats to current application state  
