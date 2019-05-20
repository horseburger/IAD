#!/usr/bin/python
import numpy as np
from Point import Point
from Centroid import Centroid
import matplotlib.pyplot as plt
import random
import sys
import argparse
from math import sqrt

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
parser.add_argument("--figures", default=2, help="Number of figures")
parser.add_argument("--no-dead", default=False, help="No dead centroids on generate", action="store_true")
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

def drawError(error, no):
    plt.axis([0, epochs, 0, 6])
    plt.title("Kohonen quantization error for " + str(args.figures) + " figures")
    plt.xlabel("Iterations")
    plt.legend(loc='upper right')
    plt.ylabel("Quantization error")
    plt.plot([i for i in range(len(error))], [i for i in error], label= str(no) + " centroids")

def generatePoints():
    if args.r:
        points = [Point(random.uniform(-5, -1), random.uniform(-1, 1)) for i in range(nPoints // 2)]
        if int(args.figures) == 2:
            for i in range(nPoints // 2):
                points.append(Point(random.uniform(1, 5), random.uniform(-1, 1)))
        return points
    if args.c:
        points = []
        while len(points) != nPoints // 2:
            tmp = Point(random.uniform(-5, -1), random.uniform(-2, 2))
            if tmp.dist(Point(-3, 0)) < 2:
                points.append(tmp)
        if int(args.figures) == 2:
            while len(points) != nPoints:
                tmp = Point(random.uniform(1, 5), random.uniform(-2, 2))
                if tmp.dist(Point(3, 0)) < 2:
                    points.append(tmp)

        random.shuffle(points)
        return points
    if args.l:
        points =  [Point(random.uniform(-7, 7), 2) for i in range(nPoints // 2)]
        if int(args.figures) == 2:
            for i in range(nPoints // 2):
                points.append(Point(random.uniform(-7, 7), -2))
        return points


def generateCentroids(points):
    centroids = [Centroid(random.uniform(-10, 10), random.uniform(-10, 10)) for i in range(nCentroids)]
    if args.no_dead:
        e = deadCentroids(points, centroids)
        while len(e) != 0:
            for i in e:
                centroids[i] = Centroid(random.uniform(-10, 10), random.uniform(-10, 10))
            e = deadCentroids(points, centroids)
    return centroids

def deadCentroids(points, centroids):
    X = [[] for i in range(len(centroids))]
    for idp, point in enumerate(points):
        l = []
        for idc, centroid in enumerate(centroids):
            l.append(point.dist(centroid))
        # r = sorted(map(lambda centroid: (centroid, point.dist(centroid)), centroids), key=lambda k: k[1])
        r = sorted([[idc, point.dist(centroid)] for idc, centroid in enumerate(centroids)], key = lambda k: k[1])[0][0]
        X[r].append(point)

    empty = []
    for idx, x in enumerate(X):
        if not x:
            empty.append(idx)
    return empty

def stdDeviation(mean, x):
    sum = 0
    for i in x:
        sum += (i - mean)**2
    return sqrt(sum / (len(x) - 1))


def run(points, centroids):  
    global l
    error = []
    prevErr = calculateError(points, centroids)
    print(prevErr)
    # drawGraph(points, centroids)

    for i in range(epochs):
        for j in range(len(points)):
            if args.k:
                k = findMinK(points[j], centroids)
                for idx, centroid in enumerate(centroids):
                    inf = influenceKohonen(idx, k)
                    centroid.updateCentroid(alpha, inf, points[j])
            if args.g:
                ranking = sorted(map(lambda centroid: (centroid, points[j].dist(centroid)), centroids), key=lambda k: k[1])
                ranking = map(lambda k: k[0], ranking)
                for idx, centroid in enumerate(ranking):
                    inf = np.exp(-idx / l)
                    centroid.updateCentroid(alpha, inf, points[j])
        l = max(3.0 - i * 0.5, 0.1)
        error.append(calculateError(points, centroids))
        print(error[-1])
        # if i < 30 or i % 25 == 0: drawGraph(points, centroids)
        random.shuffle(points)

    # drawError(error, len(centroids))

    return error[-1], deadCentroids(points, centroids)

# PART 1
# nPoints = 400
# plt.clf()
# for i in range(2, 20, 2):
#     nCentroids = i
#     points = generatePoints()
#     centroids = generateCentroids()
#     l = 3.0
#     run(points, centroids)
# plt.savefig('error')

# PART 2
nCentroids = 20
nPoints = 400

variationAlpha = [0.1, 0.3, 0.7, 0.9, 0.3, 0.9]
variationLambda = [3.0, 1.5, 4.0, 2.0, 3.0, 1.5]
for i in range(len(variationAlpha)):
    error = []
    deads = []

    alpha = variationAlpha[i]
    l = variationLambda[i]
    for j in range(100):
        points = generatePoints()
        centroids = generateCentroids(points)
        val = run(points, centroids)
        l = variationAlpha[i]
        error.append(val[0])
        deads.append(len(val[1]))

    meanError = sum(error) / len(error)
    meanDeads = sum(deads) / len(deads)
    stdDevError = stdDeviation(meanError, error)
    stdDevDeads = stdDeviation(meanDeads, deads)
    with open("2figs.txt", 'a+') as f:
        f.write("Alpha = %s\n" % alpha)
        f.write("Starting lambda: %s\n" % l)
        f.write("Number of centroids: %s\n" % nCentroids)
        f.write("Number of points: %s\n" % nPoints)
        f.write("Average error: %s\n" % meanError)
        f.write("Error standard deviation: %s\n" % stdDevError)
        f.write("Minimum error: %s\n" % min(error))
        f.write("Average dead centroids: %s\n" % meanDeads)
        f.write("Dead centroids standard deviation: %s\n\n" % stdDevDeads)




    
# error = []
# deads = []

# nCentroids = 20
# nPoints = 400
# alpha = 0.3
# l = 1.5 
# for i in range(100):
#     points = generatePoints()
#     centroids = generateCentroids()
#     val = run(points, centroids)
#     l = 1.5
#     error.append(val[0])
#     deads.append(val[1])

# meanError = sum(error) / len(error)
# meanDeads = sum(deads) / len(deads)
# stdDevError = stdDeviation(meanError, error)
# stdDevDeads = stdDeviation(meanDeads, deads)
# with open("2figs.txt", 'a+') as f:
#     f.write("Alpha = %s\n" % alpha)
#     f.write("Starting lambda: %s\n" % l)
#     f.write("Number of centroids: %s\n" % nCentroids)
#     f.write("Number of points: %s\n" % nPoints)
#     f.write("Average error: %s\n" % meanError)
#     f.write("Error standard deviation: %s\n" % stdDevError)
#     f.write("Minimum error: %s\n" % min(error))
#     f.write("Average dead centroids: %s\n" % meanDeads)
#     f.write("Dead centroids standard deviation: %s\n\n" % stdDevDeads)



# error = []
# deads = []

# nCentroids = 20
# nPoints = 400
# alpha = 0.7 
# l = 4.0
# for i in range(100):
#     points = generatePoints()
#     centroids = generateCentroids()
#     val = run(points, centroids)
#     l = 4.0
#     error.append(val[0])
#     deads.append(val[1])

# meanError = sum(error) / len(error)
# meanDeads = sum(deads) / len(deads)
# stdDevError = stdDeviation(meanError, error)
# stdDevDeads = stdDeviation(meanDeads, deads)
# with open("2figs.txt", 'a+') as f:
#     f.write("Alpha = %s\n" % alpha)
#     f.write("Starting lambda: %s\n" % l)
#     f.write("Number of centroids: %s\n" % nCentroids)
#     f.write("Number of points: %s\n" % nPoints)
#     f.write("Average error: %s\n" % meanError)
#     f.write("Error standard deviation: %s\n" % stdDevError)
#     f.write("Minimum error: %s\n" % min(error))
#     f.write("Average dead centroids: %s\n" % meanDeads)
#     f.write("Dead centroids standard deviation: %s\n\n" % stdDevDeads)



# error = []
# deads = []

# nCentroids = 20
# nPoints = 400
# alpha = 0.9 
# l = 2.0
# for i in range(100):
#     points = generatePoints()
#     centroids = generateCentroids()
#     val = run(points, centroids)
#     l = 2.0
#     error.append(val[0])
#     deads.append(val[1])

# meanError = sum(error) / len(error)
# meanDeads = sum(deads) / len(deads)
# stdDevError = stdDeviation(meanError, error)
# stdDevDeads = stdDeviation(meanDeads, deads)
# with open("2figs.txt", 'a+') as f:
#     f.write("Alpha = %s\n" % alpha)
#     f.write("Starting lambda: %s\n" % l)
#     f.write("Number of centroids: %s\n" % nCentroids)
#     f.write("Number of points: %s\n" % nPoints)
#     f.write("Average error: %s\n" % meanError)
#     f.write("Error standard deviation: %s\n" % stdDevError)
#     f.write("Minimum error: %s\n" % min(error))
#     f.write("Average dead centroids: %s\n" % meanDeads)
#     f.write("Dead centroids standard deviation: %s\n\n" % stdDevDeads)



# error = []
# deads = []

# nCentroids = 20
# nPoints = 400
# alpha = 0.9 
# l = 1.5
# for i in range(100):
#     points = generatePoints()
#     centroids = generateCentroids()
#     val = run(points, centroids)
#     l = 1.5
#     error.append(val[0])
#     deads.append(val[1])

# meanError = sum(error) / len(error)
# meanDeads = sum(deads) / len(deads)
# stdDevError = stdDeviation(meanError, error)
# stdDevDeads = stdDeviation(meanDeads, deads)
# with open("2figs.txt", 'a+') as f:
#     f.write("Alpha = %s\n" % alpha)
#     f.write("Starting lambda: %s\n" % l)
#     f.write("Number of centroids: %s\n" % nCentroids)
#     f.write("Number of points: %s\n" % nPoints)
#     f.write("Average error: %s\n" % meanError)
#     f.write("Error standard deviation: %s\n" % stdDevError)
#     f.write("Minimum error: %s\n" % min(error))
#     f.write("Average dead centroids: %s\n" % meanDeads)
#     f.write("Dead centroids standard deviation: %s\n\n" % stdDevDeads)



# error = []
# deads = []

# nCentroids = 20
# nPoints = 400
# alpha = 0.3 
# l = 3.0
# for i in range(100):
#     points = generatePoints()
#     centroids = generateCentroids()
#     val = run(points, centroids)
#     l = 3.0
#     error.append(val[0])
#     deads.append(val[1])

# meanError = sum(error) / len(error)
# meanDeads = sum(deads) / len(deads)
# stdDevError = stdDeviation(meanError, error)
# stdDevDeads = stdDeviation(meanDeads, deads)
# with open("2figs.txt", 'a+') as f:
#     f.write("Alpha = %s\n" % alpha)
#     f.write("Starting lambda: %s\n" % l)
#     f.write("Number of centroids: %s\n" % nCentroids)
#     f.write("Number of points: %s\n" % nPoints)
#     f.write("Average error: %s\n" % meanError)
#     f.write("Error standard deviation: %s\n" % stdDevError)
#     f.write("Minimum error: %s\n" % min(error))
#     f.write("Average dead centroids: %s\n" % meanDeads)
#     f.write("Dead centroids standard deviation: %s\n\n" % stdDevDeads)
