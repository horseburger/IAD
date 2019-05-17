#!/usr/bin/python
import numpy as np
from Point import Point
from Centroid import Centroid
import matplotlib.pyplot as plt
import random
import sys
import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
algs = parser.add_mutually_exclusive_group()
group.add_argument("-r", help="Draw points inside two rectangles", action="store_true")
group.add_argument("-l", help="Draw points in a line", action="store_true")
group.add_argument("-c", help="Draw points inside two circles", action="store_true")
algs.add_argument("-k", help="Use Kohonen's algorithm", action="store_true")
algs.add_argument("-g",help="Use neural gas", action="store_true")
parser.add_argument("--wta", help="Use WTA with Kohonen's algorithm (default WTM)", action="store_true")
parser.add_argument("-e", default=15, help="Number of iterations")
parser.add_argument("-n", default=10, help="Number of centroids")
parser.add_argument("-N", default=200, help="Number of points")
args = parser.parse_args()

if len(sys.argv) < 3:
    parser.print_help()
    sys.exit(1)

it = 0
epochs = int(args.e)
alpha = 0.1
l = 3.0
nCentroids = int(args.n)
nPoints = int(args.N)

def dist(a, b):
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

def findMinK(point, c):
    k = point.dist(c[0])
    q = 0
    for j in range(1, len(c)):
        d = point.dist(c[j])
        if d < k:
            k = d
            q = j

    return q

def calculateError(points, c):
    error = []
    for i in points:
        error.append(i.dist(c[findMinK(i, c)]))
    return sum(error) / len(error)

def findRo(k, i):
    return abs(k - i)

def influenceKohonen(k, kx):
    w = 0
    if args.wta:
        if k == kx:
            w = 1
        return w
    else:
        w = (findRo(k, kx)**2) / (2 * l**2)
    return np.exp(-w)

def drawGraph(points, centroids):
    plt.clf()
    plt.scatter([i.x for i in centroids], [i.y for i in centroids], s=6, c='r')
    plt.scatter([i.x for i in points], [i.y for i in points], s=2, c='k')
    plt.plot([i.x for i in centroids], [i.y for i in centroids], 'g')
    plt.axis([-10.1, 10.1, -10.1, 10.1])
    plt.grid()
    global it
    plt.savefig("plot" + str(it))
    it += 1

def generatePoints():
    if args.r:
        points = [Point(random.uniform(-5, -1), random.uniform(-1, 1)) for i in range(nPoints / 2)]
        for i in range(nPoints / 2):
            points.append(Point(random.uniform(1, 5), random.uniform(-1, 1)))
        return points
    if args.c:
        points = []
        while len(points) != nPoints / 2:
            tmp = Point(random.uniform(-5, -1), random.uniform(-2, 2))
            if tmp.dist(Point(-3, 0)) < 2:
                points.append(tmp)

        while len(points) != nPoints:
            tmp = Point(random.uniform(1, 5), random.uniform(-2, 2))
            if tmp.dist(Point(3, 0)) < 2:
                points.append(tmp)

        random.shuffle(points)
        return points
    if args.l:
        points =  [Point(random.uniform(-7, 7), 2) for i in range(nPoints / 2)]
        for i in range(nPoints / 2):
            points.append(Point(random.uniform(-7, 7), -2))
        return points


def generateCentroids():
    return [Centroid(random.uniform(-10, 10), random.uniform(-10, 10)) for i in range(nCentroids)]
    
points = generatePoints()
centroids = generateCentroids()
error = []
prevErr = calculateError(points, centroids)
print(prevErr)
drawGraph(points, centroids)

for i in range(epochs):
    for j in range(len(points)):
        if args.k:
            k = findMinK(points[j], centroids)
            for q in range(len(centroids)):
                inf = influenceKohonen(q, k)
                centroids[q].updateCentroid(alpha, inf, points[j])
        if args.g:
            ranking = sorted(map(lambda centroid: (centroid, points[j].dist(centroid)), centroids), key=lambda k: k[1])
            ranking = map(lambda k: k[0], ranking)
            for idx, centroid in enumerate(ranking):
                inf = np.exp(-idx / l)
                centroid.updateCentroid(alpha, inf, points[j])
    l = max(3.0 - i * 0.5, 0.1)
    newErr = calculateError(points, centroids)
    print(newErr)
    prevErr = newErr
    error.append(prevErr)
    if i < 30 or i % 25 == 0: drawGraph(points, centroids)
    random.shuffle(points)


plt.clf()
plt.axis([0, len(error), min(error) - 0.1, max(error) + 0.1])
plt.plot([i for i in range(len(error))], [i for i in error])
plt.savefig("error")
