
# from math import sqrt
from simul.forest import Forest
from simul.utils import dist#, bearing
# from simul.weather import Wind, Humidity
# from math import cos

class Fire():
    
    def __init__(self, params):

        self.forest = Forest(params)

        
        # distance of all trees to starting tree.
        # if the coordinates for the starting tree are not found in the forrest
        # then the closest is chosen.
        distance_lst = [(dist(k, params['fire_params']['starting_tree_coords']), k)
                        for k in self.forest.coord_dict]
        self.starting_tree_coords = min(distance_lst)[1]


    def start_fire(self):
        ''' starts fire in one tree '''

        starting_tree = self.forest.coord_dict[self.starting_tree_coords]
        starting_tree.state = 'burning'

        self.forest.tree_state['burning'].add(starting_tree)
        self.forest.tree_state['unburnt'].remove(starting_tree)

        print(starting_tree.x_y)
 
        # self.forest.tree_state['recent_burn'].add(starting_tree)


    # def potential(self):
    #     ''' generates a dictionary with the nearest trees up to a distance '''
    #     self.forest.burnable = dict()
        
    #     for t1 in self.forest.tree_lst:
    #         x, y, _ = t1.x_y
    #         x_quadrant = x // self.forest.safe_radius
    #         y_quadrant = y // self.forest.safe_radius

    #         comparable_trees = self.forest.__adjacent_trees(x_quadrant, y_quadrant)
            
    #         for t2 in comparable_trees:
    #             d = dist(t1.x_y, t2.x_y)
    #             b = bearing(t1.lat_lon, t2.lat_lon)
                
    #             fire_range = d*cos(b) * (self.wind.speed * cos(self.wind.angle))
                
    #             if 0.0 < d < self.forest.safe_radius:
    #                 if t1 in self.forest.burnable.keys():
    #                     self.forest.burnable[t1].append((d, t2))
    #                 else:
    #                     self.forest.burnable[t1] = [(d, t2)]

