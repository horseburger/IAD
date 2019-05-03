import numpy as np
import sys
import random
import matplotlib.pyplot as plt
from time import sleep
import math
import os

k = int(sys.argv[1])
epoch = int(sys.argv[2])
eps = float(sys.argv[3])



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

def generateCenters():
    c = []
    for i in range(k):
        c.append([random.uniform(-10,10), random.uniform(-10, 10)])
        random.seed(random.random())
    return c

def moveCenter(X):
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
    for i in X:
        plt.scatter([j[0] for j in i], [j[1] for j in i], s=2, c=np.random.rand(3))

    C1 = plt.Circle((-3,0), radius= 2, fill=0)
    C2 = plt.Circle((3, 0), radius=2, fill=0)
    plt.scatter([i[0] for i in c], [i[1] for i in c], s=4, c='r')
    # plt.scatter([i[0] for i in points], [i[1] for i in points], s=2)
    ax=plt.gca()
    ax.add_patch(C1)
    ax.add_patch(C2)
    plt.axis([-10.1, 10.1, -10.1, 10.1])
    plt.grid()
    plt.show()

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
c = generateCenters()


while True:
    c = generateCenters()
    flag = False

    X, error = assignPoints(points, c)
    
    for i in X:
        if not i:
            flag = True
            break
    if not flag:
        break
prevError = calcError(error)
print(prevError)

drawGraph(X, c)


for i in range(epoch):
    for j in range(len(c)):
        c[j] = moveCenter(X[j])

    X, error = assignPoints(points, c)
    newError = calcError(error)
    if abs(newError - prevError) < eps:
        break
    prevError = newError
    drawGraph(X, c)
    print(newError)