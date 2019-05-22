import numpy as np
class Centroid:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def updateCentroid(self, alpha, inf, point):
        self.x += alpha * inf * (point.x - self.x)
        self.y += alpha * inf * (point.y - self.y)

    def dist(self, centroid):
        return np.sqrt((centroid.x - self.x)**2 + (centroid.y - self.y)**2)