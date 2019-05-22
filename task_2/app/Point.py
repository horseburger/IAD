from Centroid import Centroid
import numpy as np
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def dist(self, centroid):
        return np.sqrt((centroid.x - self.x)**2 + (centroid.y - self.y)**2)