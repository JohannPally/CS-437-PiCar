import picar_4wd as fc
import numpy as np
import matplotlib.pyplot as plt
import time

class Control2:

    def __init__(self):
        fc.stop()

        self.orientation = 'N'
        self.mcodes = {b'w': "F", b's': "B", b'a': "L", b'd': "R"}
        self.next_reference = {
            'N': {'L':'W', 'F':'N', 'R':'E', 'B':'N'},
            'E': {'L':'N', 'F':'E', 'R':'S', 'B':'E'},
            'S': {'L':'E', 'F':'S', 'R':'W', 'B':'S'},
            'W': {'L':'S', 'F':'W', 'R':'N', 'B':'W'}
        }
       
        self.traveled = 0
        return
        
    def move(self, code):
        movement = self.mcodes.get(code)

        if movement is not None:
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

            self.traveled += 15.24
            self.orientation = self.next_reference[self.orientation][movement]
        
        else:
            print('INVALID MOVEMENT CODE')

        return self.orientation, self.traveled
    
