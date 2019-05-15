import matplotlib.pyplot as plt
import random
import math
import sys
import subprocess
import imageio
import numpy as np


mode = 0 if sys.argv[1] == "WTA" else 1
eps = 0.001
l = 3.0
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
    plt.plot([i[0] for i in c], [i[1] for i in c], 'g')
    plt.axis([-10.1, 10.1, -10.1, 10.1])
    plt.grid() 
    global it
    plt.savefig("plot" + str(it))
    it += 1
    # plt.show()

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

def findRo(k, i):
    return abs(k - i)

def influence(k, kx):
#     w = [0 for i in range(len(c))]
#     if not mode:
#         w[k] = 1
#         return w
#     for i in range(len(c)):
#         w[i] =  (findRo(k, i)**2) / (2 * l**2)
#         w[i] = -w[i]

#     return w
    w = 0
    if not mode:
        if k == kx:
            w = 1
        return w
    else:
        w = (findRo(k, kx)**2) / (2 * l**2)
    return np.exp(-w)

points = generatePoints()
c = generateCentroids()
error = []
prevErr = calculateError(points, c)
print(prevErr)
drawGraph(points, c)

for i in range(int(sys.argv[2])):
    for j in range(len(points)):
        k = findMinK(points[j], c)
        for q in range(len(c)):
            inf = influence(q, k)
            c[q][0] = c[q][0] + alpha * inf * (points[j][0] - c[q][0])
            c[q][1] = c[q][1] + alpha * inf * (points[j][1] - c[q][1])
        if j % 10 == 0 and l > 0.01:
            l -= 0.005
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
