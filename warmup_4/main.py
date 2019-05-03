import numpy as np
import sys
import random
import matplotlib.pyplot as plt
from time import sleep
import math
import os

if len(sys.argv) < 3:
    print("Usage main.py <no. of centroids> <iterations> <epsilon>")
    sys.exit()

k = int(sys.argv[1])
epoch = int(sys.argv[2])
eps = float(sys.argv[3])
filenameIter = 0

def dist(a, b):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

def calcError(error):
    return sum(error) / len(error)

def minInList(list):
    m = list[0]
    j = 0
    for i in range(1, len(list)):
        if list[i] < m:
            m = list[i]
            j = i
    return j

def generateCentroids():
    c = []
    for i in range(k):
        c.append([random.uniform(-10,10), random.uniform(-10, 10)])
        random.seed(random.random())
    return c

def correctCentroids(c, empty):
    for i in empty:
        c[i] = [random.uniform(-10, 10), random.uniform(-10, 10)]
        random.seed(random.random())
    return c


def moveCentroid(X):
    sumX = 0
    sumY = 0
    for i in X:
        sumX += i[0]
        sumY += i[1]
    newC = [sumX / len(X), sumY / len(X)]
    return newC

def assignPoints(points, c):
    X = [[] for i in range(k)]
    error = []
    for i in range(len(points)):
        l = []
        for j in range(len(c)):
            l.append(dist(points[i], c[j]))
        r = minInList(l)
        X[r].append(points[i])
        error.append(dist(X[r][-1], c[r]))

    return X, error

def drawGraph(X, c):
    plt.clf()

    # C1 = plt.Circle((-3,0), radius= 2, fill=0)
    # C2 = plt.Circle((3, 0), radius=2, fill=0)
    plt.scatter([i[0] for i in points], [i[1] for i in points], s=2, c='k')
    plt.scatter([i[0] for i in c], [i[1] for i in c], s=6, c='r')
    # ax=plt.gca()
    # ax.add_patch(C1)
    # ax.add_patch(C2)
    plt.axis([-10.1, 10.1, -10.1, 10.1])
    plt.grid()
    global filenameIter 
    plt.savefig("plot" + str(k) + "_" + str(filenameIter))
    filenameIter += 1
    # plt.show()``


c1 = [-3, 0]
c2 = [3, 0]
points = []

while len(points) != 100:
    tmp = [random.uniform(-5, -1), random.uniform(-2, 2)]
    if dist(tmp, c1) < 2:
        points.append(tmp)

while len(points) != 200:
    tmp = [random.uniform(1, 5), random.uniform(-2, 2)]
    if dist(tmp, c2) < 2:
        points.append(tmp)

random.shuffle(points)
c = generateCentroids()


while True:
    flag = False

    X, error = assignPoints(points, c)
    empty = []

    for i in range(len(X)):
        if not X[i]:
            empty.append(i)
            flag = True
            break
    if not flag:
        break
    c = correctCentroids(c, empty)

        
prevError = calcError(error)
finalErr = [prevError]
print(prevError)
drawGraph(X, c)


for i in range(epoch):
    for j in range(len(c)):
        c[j] = moveCentroid(X[j])

    X, error = assignPoints(points, c)
    newError = calcError(error)
    finalErr.append(newError)
    if abs(newError - prevError) < eps:
        break
    prevError = newError
    drawGraph(X, c)
    print(newError)

plt.clf()
plt.axis([0, len(finalErr), min(finalErr) - 0.1, max(finalErr) + 0.1])
plt.grid()
plt.plot([i for i in range(len(finalErr))], finalErr)
plt.savefig("error" + str(k))
