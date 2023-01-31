import picar_4wd as fc
import numpy as np
import matplotlib.pyplot as plt
import time
from astar import AStar

class Control:

    def __init__(self):
        self.local_size = 13
        self.grid = np.zeros((100,100))
        
        self.orientation = 'S'
        self.location = (0,50)
        
        self.next_reference = {
            'N': {(-1,0): ('L','W'), (0,-1): ('F','N'), (1,0): ('R','E')},
            'E': {(0,-1): ('L','N'), (1,0): ('F','E'), (0,1): ('R','S')},
            'S': {(1,0): ('L','E'), (0,1): ('F','S'), (-1,0): ('R','W')},
            'W': {(0,1): ('L', 'S'), (-1,0): ('F','W'), (0,-1): ('R','N')}
        }
        return
    
    def update_attributes(self, location = None, orientation = None):
        if location is not None:
            self.location = location
        if orientation is not None:
            self.orientation = orientation
    
#MOVEMENT
    
    def step(self, path):
        next_loc = path.pop(0)
        diff = (next_loc[0]-self.location[0], next_loc[1]-self.location[1])
        mvmnt, nxt_or = self.next_reference[self.orientation][diff]
        print(self.location, self.orientation, next_loc, mvmnt)
        self.move(mvmnt, nxt_or)
        self.location = next_loc
        return path
    
    def move(self, movement, next_orientation):
        if movement == 'L':
            fc.stop()
            fc.turn_left(50)
            time.sleep(1)
            fc.forward(50)

        elif movement == 'F':
            fc.forward(50)
        
        elif movement == 'R':
            fc.stop()
            fc.turn_right(50)
            time.sleep(1)
            fc.forward(50)
        
        self.orientation = next_orientation
        return
        
    
#SCANNING
    
    def update_grid(self, angle, dist):
        x = dist*np.cos((angle+90)*np.pi/180)
        y = dist*np.sin((angle+90)*np.pi/180)
        
        mid = int(self.mat_size/2)
        dis_factor = 3
        xi = mid+int(x//dis_factor)
        yi = int(y//dis_factor)
        
        self.update_global(xi,yi)
    
    def get_global_index(self, x, y):
        I, J = self.location
        
        if self.orientation == 'N':
            return (I+x, J-y)
        
        elif self.orientation == 'E':
            return (I+y, J+x)
            
        elif self.orientaiton == 'S':
            return (I-x, J+y)
            
        elif self.orientation == 'W':
            return (I-y, J-x)
    
    def update_global(self, x, y):
        gi, gj = self.get_global_index(x,y)
        self.grid[gi][gj] = 1
        return
        
    
    def scan_env(self):
        fc.get_distance_at(-90)
        for i in range(-90,90,10):
            z = fc.get_distance_at(i)
            self.update_grid(i,z)

        for i in range(90,-91,-10):
            z = fc.get_distance_at(i)
            self.update_grid(i,z)
        
        fc.get_distance_at(0)
        return
    
#TESTING

if __name__ == '__main__':
    cnt = Control()
    cnt.update_attributes((95,95),'N')
    astar = AStar()
    pt = astar.compute(cnt.grid, cnt.location)
    
    """
    cnt.update_attributes((0,0),'N')
    pt = [(1,0), (2,0), (2,1), (3,1)]
    while len(pt) > 0:
        pt = cnt.step(pt)
    """
    