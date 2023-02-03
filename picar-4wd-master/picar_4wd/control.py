import picar_4wd as fc
import numpy as np
import matplotlib.pyplot as plt
import time
from astar import AStar
from vision import Vision

class Control:

    def __init__(self):
        fc.stop()
        self.global_size = 7
        self.local_size = 4
        self.dis_factor = 15
        self.cycle_length = 5
        self.grid = np.zeros((self.global_size, self.global_size))
        
        self.orientation = 'S'
        self.location = (0,50)
        self.ast = AStar(self.global_size)
        self.vision = Vision()
        self.vision_memory = True
        
        self.next_reference = {
            'N': {(0,-1): ('L','W'), (-1,0): ('F','N'), (0,1): ('R','E'), (1,0): ('B','N')},
            'E': {(-1,0): ('L','N'), (0,1): ('F','E'), (1,0): ('R','S'), (0,-1): ('B','E')},
            'S': {(0,1): ('L','E'), (1,0): ('F','S'), (0,-1): ('R','W'), (-1,0): ('B','S')},
            'W': {(1,0): ('L', 'S'), (0,-1): ('F','W'), (-1,0): ('R','N'), (0,1): ('B','W')}
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
        self.print_env(path)
        if len(path) == 0:
            return False
        #print('printing env')
        for i in range(self.cycle_length):
            path = self.step(path)
            print('one step done')
            #if fc.get_distance_at(0) < 3:
                #return True
            if self.vision_memory and self.vision.check_stop_sign():
                fc.stop()
                time.sleep(5)
                self.vision_memory = False
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
            time.sleep(.1)
            fc.turn_left(50)
            time.sleep(1)
            fc.stop()
            time.sleep(.1)
            fc.forward(20)

        elif movement == 'F':
            fc.forward(20)

        elif movement == 'B':
            fc.stop()
            time.sleep(.1)
            fc.backward(20)
        
        elif movement == 'R':
            fc.stop()
            time.sleep(.1)
            fc.turn_right(60)
            time.sleep(.9)
            fc.stop()
            time.sleep(.1)
            fc.forward(20)
        
        time.sleep(.7)
        fc.stop()
        self.orientation = next_orientation
        return
        
    
# SCANNING
    
    def get_global_index(self, x, y):
        I, J = self.location
        
        if self.orientation == 'N':
            return (I-y, J+x)
        
        elif self.orientation == 'E':
            return (I+x, J+y)
            
        elif self.orientation == 'S':
            return (I+y, J-x)
            
        elif self.orientation == 'W':
            return (I-x, J-y)
    
    def update_global(self, x, y):
        gi, gj = self.get_global_index(x,y)
        itest = gi >= 0 and gi < self.global_size
        jtest = gj >= 0 and gj < self.global_size

        if itest and jtest:
            self.grid[gi][gj] = 1

        return

    def update_grid(self, angle, dist):
        x = (dist*np.cos((angle+90)*np.pi/180))//self.dis_factor
        y = (dist*np.sin((angle+90)*np.pi/180))//self.dis_factor

        xi = int(x)
        yi = int(y)
        
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
        for i in range(-90,90,3):
            z = fc.get_distance_at(i)
            if z > 0:
                self.update_grid(i,z)

        for i in range(90,-91,-3):
            z = fc.get_distance_at(i)
            if z > 0:
                self.update_grid(i,z)
        
        fc.get_distance_at(0)
        return
        
    
# TESTING

if __name__ == '__main__':
    cnt = Control()
    cnt.update_attributes((cnt.global_size-1,cnt.global_size-2),'N')
        
    #FINAL MOVEMENT
    while(True):
        if not cnt.cycle():
            break
    
    """
    #TESTING VISION
    for i in range(10):
        cnt.vision.check_stop_sign()
        print("took photo, waiting on input")
        input()
    """
    
    """
    # TESTING MOVEMENT
    cnt.move('R', 'N')
    fc.stop()
    input()
    cnt.move('L', 'N')
    fc.stop()
    input()
    cnt.move('F', 'N')
    fc.stop()
    input()
    cnt.move('B', 'N')
    fc.stop()
    """

    """
    # SCANNING
    cnt.update_attributes((20,10),'N')
    for _ in range(10):
        cnt.grid = np.zeros((cnt.global_size, cnt.global_size))
        cnt.scan_env()  
        cnt.print_env()
    """

    """
    # ENVIRONMENT UPDATE
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
    