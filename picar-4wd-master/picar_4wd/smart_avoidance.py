import picar_4wd as fc
import numpy as np
import matplotlib.pyplot as plt

class Avoid():
    
    def __init__(self):
        self.mat_size = 13
        self.grid = np.zeros((self.mat_size,self.mat_size))
        return
    
    def update_grid(self, angle, dist):
        x = dist*np.cos((angle+90)*np.pi/180)
        y = dist*np.sin((angle+90)*np.pi/180)
        
        mid = int(self.mat_size/2)
        dis_factor = 3
        xi = mid+int(x//dis_factor)
        yi = int(y//dis_factor)
        
        print(angle, dist, xi, yi)
        
        pos_check = xi > 0 and yi > 0
        less_check = xi < self.mat_size and yi < self.mat_size
        
        if pos_check and less_check:
            self.grid[yi,xi] = 1
        
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
    
    def print_grid(self):
        plt.matshow(self.grid)
        plt.show()

if __name__ == "__main__":
    avoid = Avoid()
    avoid.scan_env()
    avoid.print_grid()
    