class Centroid:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def updateCentroid(self, alpha, inf, point):
        self.x += alpha * inf * (point.x - self.x)
        self.y += alpha * inf * (point.y - self.y)