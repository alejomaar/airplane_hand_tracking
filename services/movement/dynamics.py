from datetime import datetime, timedelta
from typing import Dict, Tuple
import numpy as np
from numpy import array
     
class Dynamics():
    
    def __init__(self):
        self.position = np.empty((0, 2))
        self.velocity = np.empty((0, 2))
        self.time = []
        self.kernel = np.array([0.18, 0.32, 0.5])
        
    def add_vector(self,new_vector:array):
        t = datetime.now()        
        if self.position.size > 0:
            t0 = self.time[-1]
            dt = (t - t0).total_seconds()
            v = (new_vector - self.position[-1]) / dt
        else:
            v = np.zeros(2)
        self.position = np.append(self.position, [new_vector], axis=0)
        self.time.append(datetime.now()) 
        self.velocity = np.append(self.velocity, [v], axis=0)
        
        
    def calculate_velocity(self):
        if self.position.shape[0] < 4:
            return (0,0)
        return self.kernel@self.velocity[-3:]