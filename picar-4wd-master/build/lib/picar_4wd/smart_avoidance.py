import picar_4wd as fc
import numpy as np

class Avoid():
    
    def __init__(self):
        return
    
    def update_grid(self, angle, dist):
        x = dist*np.cos((angle+90)*np.pi/180)/3
        y = dist*np.sin((angle+90)*np.pi/180)/3
        print(angle, dist, x, y)
        
    def scan_env(self):
        for i in range(-90,90,10):
            z = fc.get_distance_at(i)
            self.update_grid(i,z)
        for i in range(90,-90,-10):
            z = fc.get_distance_at(i)
            self.update_grid(i,z)
        
        return

if __name__ == "__main__":
    avoid = Avoid()
    avoid.scan_env()