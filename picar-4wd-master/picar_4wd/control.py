import picar_4wd as fc
import numpy as np
import matplotlib.pyplot as plt

class Control:

    def __init__(self):
        self.orientation = None
        self.location = None
        self.path = None
        self.next_reference = {
            'N': {(-1,0): ('L','W'), (0,-1): ('F','N'), (1,0): ('R','E')},
            'E': {(0,-1): ('L','N'), (1,0): ('F','E'), (0,1): ('R','S')},
            'S': {(1,0): ('L','E'), (0,1): ('F','S'), (-1,0): ('R','W')},
            'W': {(0,1): ('L', 'S'), (-1,0): ('F','W'), (0,-1): ('R','N')}
        }
        return
    
    def step(self):
        next = self.path.pop(0)
        diff = next - self.location
        mvmnt, nxt_or = self.next_reference[self.orientation][diff]
        self.move(mvmnt, nxt_or)
        return

    def update(self, path = None, location = None, orientation = None):
        if path is not None:
            self.path = path
        if location is not None:
            self.location = location
        if orientation is not None:
            self.orientation = orientation
    
    def move(self, movement, next_orientation):
        if movement == 'L':
            fc.stop()
            fc.turn_left(50)
            #TODO wait?
            fc.forward(50)

        elif movement == 'F':
            fc.forward(50)
        
        elif movement == 'R':
            fc.stop()
            fc.turn_right(50)
            #TODO wait?
            fc.forward(50)
        
        self.orientation = next_orientation
        return