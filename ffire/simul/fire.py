
from collections import Counter

from simul.forest import Forest
from simul.utils import dist, sigmoid#, bearing
from simul.weather import Wind, Humidity
 

class Fire():
    
    def __init__(self, params):

        self.forest = Forest(params)
        self.wind = Wind(params)

        
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


    def fire_potential(self, t1):
        '''
        Receives an unburnt or ember tree
        '''
        x, y, _ = t1.x_y
        x_quadrant = x // self.forest.safe_radius
        y_quadrant = y // self.forest.safe_radius 

        neighbour_trees = self.forest.adjacent_trees(x_quadrant, y_quadrant) 
        burning_neighbours = [t for t in neighbour_trees if t.state == 'burning'] 
        
        if len(burning_neighbours) == 0:
            pass
        else:
            cnt = 0
            dist_lst = list()
            
            for t2 in burning_neighbours:
                x2, y2, _ = t2.x_y
                A,B,C,D = self.wind.fire_projection(x2, y2, self.forest.safe_radius)
                extremes = [(min(p), max(p))for p in zip(A,B,C,D)]
                
                if (extremes[0][0] <= x <= extremes[0][1] 
                    and extremes[1][0] <= y <= extremes[1][1]):
                    cnt += 1 
                    dist_lst.append(dist(t1.x_y, t2.x_y))
                if len(dist_lst) > 0:
                    mean_distance = sum(dist_lst) / len(dist_lst)
                    factor = cnt / (mean_distance +1)
                    # print(cnt, factor, sigmoid(factor))
                else:
                    factor = 0.0
            t1.burning_prob = sigmoid(factor) * 0.8
        
 
