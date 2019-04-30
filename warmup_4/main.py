import numpy as np
import sys
import random
import matplotlib.pyplot as plt
from time import sleep
import math
import os

def dist(a, b):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

# def error(a, b):
#     sum = 0 
#     for i in range(len(a)):
#         sum += dist(a[i], b[i])
#     return sum / len(a)

def minInList(list):
    m = list[0]
    j = 0
    for i in range(1, len(list)):
        if list[i] < m:
            m = list[i]
            j = i
    return j

p1 = []
p2 = []
c1 = [-3, 0]
c2 = [3, 0]

while len(p1) != 100:
    tmp = [random.uniform(-5, -1), random.uniform(-2, 2)]
    if dist(tmp, [-3, 0]) < 2:
        p1.append(tmp)

while len(p2) != 100:
    tmp = [random.uniform(1, 5), random.uniform(-2, 2)]
    if dist(tmp, [3, 0]) < 2:
        p2.append(tmp)

k = int(sys.argv[1])
r = []
for i in range(k):
    r.append([random.uniform(-8, 8), random.uniform(-8, 8)])
    random.seed(random.random())


X = [[] for i in range(k)]

error = []

for i in range(len(p1)):
    l1 = []
    l2 = []
    for j in range(len(r)):
        l1.append(dist(p1[i], r[j]))        
        l2.append(dist(p2[i], r[j]))
        error.append(l1[-1])
        error.append(l2[-1])
    X[minInList(l1)].append(p1[i])
    X[minInList(l2)].append(p2[i])

c1 = plt.Circle((-3,0), radius= 2, fill=0)
c2 = plt.Circle((3, 0), radius=2, fill=0)

print(sum(error) / len(error))

for i in X:
    plt.scatter([j[0] for j in i], [j[1] for j in i], s=2, c=np.random.rand(3))




plt.scatter([i[0] for i in r], [i[1] for i in r], s=4, c='r')
ax=plt.gca()
ax.add_patch(c1)
ax.add_patch(c2)
plt.axis([-10, 10, -10, 10])
plt.grid()
plt.show()