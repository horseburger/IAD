import numpy as np 
import matplotlib.pyplot as plt
import math
import random


def generateCenters(k):
    return [random.uniform(0, 10) for i in range(k)]

def generateSigm(k):
    return [random.uniform(0, 10) for i in range(k)]

def generateWeights(k):
    return [random.uniform(-4, 4) for i in range(k + 1)]

def dist(a, b):
    return abs(a - b)

def calculateOutput(weights, z):
    sum = weights[0]
    for i in range(1, len(weights)):
        sum += weights[i] * z[i - 1]
    return sum


def gaussFunction(d, sigm):
    return np.exp(-(d**2 / 2.0 * (sigm)**2))

def calculateRadial(x, c, sigm):
    return gaussFunction(dist(x, c), sigm)


k = 4
centers = sorted(generateCenters(k))
sigms = generateSigm(k)
weights = generateWeights(k)

x = [i for i in np.arange(0, 10, 0.01)]

y = []
z = []
for point in x:
    z.append([calculateRadial(point, center, sigms[j]) for j, center in enumerate(centers)])

for i in range(1, k + 1):
    plt.plot([j for j in x], [j[i - 1] * weights[i] for j in z], 'r')

for radial in z:
    y.append(calculateOutput(weights, radial))

plt.plot([i for i in x], [i for i in y], 'k')
plt.grid()
plt.show()
