import picar_4wd as fc
import numpy as np
import matplotlib.pyplot as plt
import time
from astar import AStar

class Control:

    def __init__(self):
        self.global_size = 30
        self.local_size = 10
        self.dis_factor = 10
        self.grid = np.zeros((self.global_size, self.global_size))
        
        self.orientation = 'S'
        self.location = (0,50)
        self.ast = AStar()
        
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
    
    def cycle(self):
        self.scan_env()
        print('done scanning')
        path = self.ast.compute(self.grid, self.location)
        if len(path) == 0:
            return False
        self.print_env(path)
        print('printing env')
        for i in range(10):
            path = self.step(path)
            print('one step done')
        return True
        
    
#MOVEMENT
    
    # MAIN PATH TREADING FUNCTION
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
            time.sleep(.8)
            fc.forward(50)
            time.sleep(.5)

        elif movement == 'F':
            fc.forward(50)
            time.sleep(.5)
        
        elif movement == 'R':
            fc.stop()
            fc.turn_right(50)
            time.sleep(.8)
            fc.forward(50)
            time.sleep(.5)
        
        self.orientation = next_orientation
        return
        
    
# SCANNING
    
    def get_global_index(self, x, y):
        I, J = self.location
        
        if self.orientation == 'N':
            return (I+x, J-y)
        
        elif self.orientation == 'E':
            return (I+y, J+x)
            
        elif self.orientation == 'S':
            return (I-x, J+y)
            
        elif self.orientation == 'W':
            return (I-y, J-x)
    
    def update_global(self, x, y):
        gi, gj = self.get_global_index(x,y)
        itest = gi >= 0 and gi < 100
        jtest = gj >= 0 and gj < 100

        if itest and jtest:
            self.grid[gi][gj] = 1

        return

    def update_grid(self, angle, dist):
        x = dist*np.cos((angle+90)*np.pi/180)
        y = dist*np.sin((angle+90)*np.pi/180)
        
        mid = int(self.local_size/2)
        
        xi = mid+int(x//self.dis_factor)
        yi = int(y//self.dis_factor)
        
        self.update_global(xi,yi)

    def print_env(self, path = []):
        tmp_grid = np.copy(self.grid)

        for step in path:
            si, sj = step
            tmp_grid[si][sj] = 3

        ri, rj = self.location
        tmp_grid[ri][rj] = 4
        tmp_grid[0][0] = 5

        plt.matshow(tmp_grid)
        plt.show()
        
    # MAIN SANNING FUNCTION
    def scan_env(self):
        fc.stop()
        fc.get_distance_at(-90)
        for i in range(-90,90,10):
            z = fc.get_distance_at(i)
            self.update_grid(i,z)

        for i in range(90,-91,-10):
            z = fc.get_distance_at(i)
            self.update_grid(i,z)
        
        fc.get_distance_at(0)
        return
    
# TESTING

if __name__ == '__main__':
    fc.stop()
    cnt = Control()
    ast = AStar()
    cnt.update_attributes((cnt.global_size-2,cnt.global_size-2),'N')

    while(True):
        if not cnt.cycle():
            break

    """
    # ENVIRONMENT SCANNING
    cnt.update_attributes((80,50),'N')
    cnt.scan_env()
    path = ast.compute(cnt.grid, cnt.location)
    cnt.print_env(path)

    cnt.update_attributes((60,50),'E')
    cnt.scan_env()
    path = ast.compute(cnt.grid, cnt.location)
    cnt.print_env(path)

    cnt.update_attributes((40,50),'S')
    cnt.scan_env()
    path = ast.compute(cnt.grid, cnt.location)
    cnt.print_env(path)

    cnt.update_attributes((20,50),'W')
    cnt.scan_env()
    path = ast.compute(cnt.grid, cnt.location)
    cnt.print_env(path)
    """

    """ 
    # ASTAR
    astar = AStar()
    pt = astar.compute(cnt.grid, cnt.location)
    """
    
    """
    # PATH FINDING
    cnt.update_attributes((0,0),'N')
    pt = [(1,0), (2,0), (2,1), (3,1)]
    while len(pt) > 0:
        pt = cnt.step(pt)
    """
    