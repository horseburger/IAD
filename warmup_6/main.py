import matplotlib.pyplot as plt
import random
import math
import sys
import subprocess
import numpy as np


l = 2.5
alpha = 0.1
it = 0
nCentroids = 10
def dist(a, b):
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)



def generatePoints():
    points = []
    while len(points) != 100:
        tmp = [random.uniform(-5, -1), random.uniform(-2, 2)]
        if dist(tmp, [-3, 0]) < 2:
            points.append(tmp)

    while len(points) != 200:
        tmp = [random.uniform(1, 5), random.uniform(-2, 2)]
        if dist(tmp, [3, 0]) < 2:
            points.append(tmp)

    random.shuffle(points)
    return points


def generateCentroids():
    c = []
    for i in range(nCentroids):
        c.append([random.uniform(-10, 10), random.uniform(-10, 10)])
        random.seed(random.random())

    return c

def drawGraph(X, c):
    plt.clf()

    plt.scatter([i[0] for i in X], [i[1] for i in X], s=2, c='k')
    plt.scatter([i[0] for i in c], [i[1] for i in c], s=6, c='r')
    #plt.plot([i[0] for i in c], [i[1] for i in c], 'r')
    plt.axis([-10.1, 10.1, -10.1, 10.1])
    plt.grid() 
    global it
    plt.savefig("plot" + str(it))
    it += 1
    # plt.show()

def sortC(point, c):
    d = []
    for i in range(len(c)):
        d.append([i, dist(point, c[i])])
    
    for i in range(len(c)):
        for j in range(len(c) - 1):
            if d[j][1] > d[j + 1][1]:
                tmp = d[j]
                d[j] = d[j + 1]
                d[j + 1] = tmp
    i = []
    for j in range(len(d)):
        i.append(d[j][0])


    return i


def findMinK(point, c):
    k = dist(point, c[0])
    q = 0
    for j in range(1, len(c)):
        d = dist(point, c[j])
        if d < k:
            k = d
            q = j

    return q

    
            
def calculateError(points, c):
    error = []
    for i in range(len(points)):
        error.append(dist(points[i], c[findMinK(points[i], c)]))
    return sum(error) / len(error)


# sort by distance to point and 'i' is the distance in the sorted list

points = generatePoints()
c = generateCentroids()
error = []
prevErr = calculateError(points, c)
print(prevErr)
drawGraph(points, c)

for i in range(int(sys.argv[1])):
    for j in range(len(points)):
        # map returns a tuple consisting of (x, y), distance from point to centroid
        ranking = sorted(map(lambda centroid: (centroid, dist(points[j], centroid)), c), key=lambda k: k[1])
        ranking = map(lambda k: k[0], ranking)
        for idx, centroid in enumerate(ranking): 
            inf = np.exp(-idx / l)
            centroid[0] = centroid[0] + alpha * inf * (points[j][0] - centroid[0])
            centroid[1] = centroid[1] + alpha * inf * (points[j][1] - centroid[1])
    l = max(2.5 - i * 0.5, 0.1)
    newErr = calculateError(points, c)
    print(newErr)
    prevErr = newErr
    error.append(prevErr)
    if i < 30 or i % 25 == 0: drawGraph(points, c)
    random.shuffle(points)

plt.clf()
plt.axis([0, len(error), min(error) - 0.1, max(error) + 0.1])
plt.plot([i for i in range(len(error))], [i for i in error])
plt.savefig("error")
