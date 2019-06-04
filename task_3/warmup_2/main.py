import matplotlib.pyplot as plt
import numpy as np
import random
import math

def readData(filename):
    data = []
    with open(filename, "r") as f:
        data.append(f.readlines())
    coords = sorted(map(lambda k: k.strip('\n').split(' '), data[0]), key=lambda k: float(k[0]))
    
    return list(map(lambda k: float(k[0]), coords)), list(map(lambda k: float(k[1]), coords))

def generateCenters(k, x):
    return [x[random.randint(0, len(x) - 1)] for i in range(k)]

def generateWeights(k):
    return [random.random() for i in range(k+1)]

def generateSigmas(centers, k):
    max = 0
    for i in range(k):
        for j in range(k):
            d = np.linalg.norm(centers[i] - centers[j])
            if d > max:
                max = d
    d = max
    return d / math.sqrt(2*k)

def dist(a, b):
    return abs(a - b)

def calculateOutput(weights, z):
    sum = weights[0]
    for i in range(1, len(weights)):
        sum += weights[i] * z[i - 1]
    return sum

def gaussFunction(d, sigm):
    return np.exp(-((d**2) / (2.0 * (sigm)**2)))

def calculateRadial(x, c, sigm):
    return gaussFunction(dist(x, c), sigm)

def calculateError(f, y):
    sum = 0
    for i in range(len(f)):
        sum += (f[i] - y[i])**2
    return sum / (2.0 * len(f))
    # return (f - y)**2 / 2

def partialDerivative(f, y, z):
    # sum = 0
    # for i in range(len(f)):
        # sum += (f[i] - y[i]) * z
    # return (sum / len(f))
    return ((f - y) * z) / 2

def findParams(x):
    error = []
    for i in range(iterations):
        radials = []
        output = []
        for idx in range(len(x)):
            radialZ = list(map(calculateRadial, [x[idx] for j in range(k)], centers, [sigma for j in range(k)]))
            output.append(calculateOutput(weights, radialZ))
            radials.append(radialZ)


            if learn:
                for idw in range(len(weights)):
                    weights[idw] -= alpha * partialDerivative(output[-1], y[idx], 1 if not idw else radialZ[idw - 1])
        # err = calculateError(output, y)
        error.append(calculateError(output, y))
        if i % 200 == 0:
            print(error[-1])
        if not learn:
            return output
    

    return radials, error


k = 10
iterations = 5000
alpha = 0.01
eps = 0.01
learn = True

x, y = readData("data.txt")
centers = generateCenters(k, x)
sigma = generateSigmas(centers, k)
# sigma = [random.uniform(0, 3) for i in range(k)]
weights = generateWeights(k)

radials, error = findParams(x)
plt.plot([i for i in range(len(error))], [i for i in error])
plt.savefig("error")
plt.clf()
for idr in range(1, k + 1):
    plt.plot([i for i in x], [z[idr - 1] * weights[idr] for z in radials], 'r')
x, y = readData("test.txt")
t = np.arange(min(x), max(x), 0.1)
plt.scatter([i for i in x], [i for i in y], s=2, c='g')
learn = False
plt.plot([i for i in x], [i for i in findParams(x)], 'b')
plt.scatter([center for center in centers], [0 for i in range(len(centers))])
plt.show()