import picar_4wd as fc

class Avoid():
    
    def __init__(self):
        return
    
    def update_grid(self, angle, distance):
        
    
    def scan_env(self):
        for i in range(-90,90,10):
            fc.get_distance_at(i)
        
        for i in range(90,-90,-10):
            fc.get_distance_at(i)
        
        return

if __name__ == "__main__":
    avoid = Avoid()
    avoid.scan_env()