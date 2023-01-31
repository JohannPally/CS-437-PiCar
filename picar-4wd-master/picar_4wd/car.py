from control import Control
from scan import Scan

class Car:
    
    def __init__(self):
        self.C = Control()
    
    def update_environment(self):
        