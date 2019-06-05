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

def stdDeviation(mean, x):
    sum = 0
    for i in x:
        sum += (i - mean)**2
    return math.sqrt(sum / (len(x) - 1))


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
    sum = 0
    for i in range(len(f)):
        sum += (f[i] - y[i]) * z[i]
    return (sum / len(f))
    # return ((f - y) * z) / 2

def findParams(x):
    error = []
    it = 0
    step = int(iterations / 6)
    for i in range(iterations):
        radials = []
        output = []
        for idx in range(len(x)):
            radials.append(list(map(calculateRadial, [x[idx] for j in range(k)], centers, [sigma for j in range(k)])))
            output.append(calculateOutput(weights, radials[-1]))


            # if learn:
            #     for idw in range(len(weights)):
            #         weights[idw] -= alpha * partialDerivative(output[-1], y[idx], [1 if not idw else radial[idw - 1] for radial in radials] )
        if learn:
            for idw in range(len(weights)):
                weights[idw] -= alpha * partialDerivative(output, y, [1 if not idw else radial[idw - 1] for radial in radials] )
        error.append(calculateError(output, y))
        if i % step == 0 and midDraw:
            plt.plot(x, output, label="Part " + str(it))
            it += 1
            print("Checkpoint")
        if i % 200 == 0:
            print(error[-1])
        if learn and error[-1] < eps:
            break
        if not learn:
            return output
    

    return radials, error


iterations = 15000
alpha = 0.01
eps = 0.1
learn = True
midDraw = False

# PART 1
# small [0.1, .8) the error was much bigger than that when using an optimized sigma
# big [2.0, 3.5)
# for k in range(1, 42, 10):
#     x, y = readData("data.txt")
#     if k == 1:
#         plt.scatter(x, y, s=1, c='g', label="Training data")
#     learn = True
#     centers = generateCenters(k, x)
#     sigma = random.uniform(2.0, 3.5)
#     weights = generateWeights(k)
#     findParams(x)
#     learn = False
#     x, y = readData("test.txt")
#     if k == 1:
#         plt.scatter(x, y, s=1, c='r', label="Test data")
#     plt.plot(x, [i for i in findParams(x)], label=str(k) + "neurons")
# plt.legend()
# plt.grid()
# plt.savefig("big_sigma")

# PART 2
# k = 11
# plt.title("Plot for small sigma")
# x, y = readData("data.txt")
# plt.scatter(x, y, s=1, c='g', label="Training data")
# centers = generateCenters(k, x)
# sigma = random.uniform(0.1, 0.8)
# weights = generateWeights(k)
# radials = findParams(x)[0]
# for q in range(1, k + 1):
#     plt.plot(x, [radial[q - 1] * weights[q] for radial in radials], 'r')
# x, y = readData("test.txt")
# plt.scatter(x, y, s=1, c='b', label="Test data")
# learn = False
# plt.plot(x, findParams(x), label="Final result")
# plt.legend()
# plt.grid()
# plt.savefig("point2_smallSigma")


# k = 11
# plt.clf()
# plt.title("Plot for big sigma")
# learn = True
# x, y = readData("data.txt")
# plt.scatter(x, y, s=1, c='g', label="Training data")
# centers = generateCenters(k, x)
# sigma = random.uniform(2.0, 3.5)
# weights = generateWeights(k)
# radials = findParams(x)[0]
# for q in range(1, k + 1):
#     plt.plot(x, [radial[q - 1] * weights[q] for radial in radials], 'r')
# x, y = readData("test.txt")
# plt.scatter(x, y, s=1, c='b', label="Test data")
# learn = False
# plt.plot(x, findParams(x))
# plt.legend()
# plt.grid()
# plt.savefig("point2_bigSigma")

# k = 11
# plt.clf()
# plt.title("Plot for optimal sigma")
# learn = True
# x, y = readData("data.txt")
# plt.scatter(x, y, s=1, c='g', label="Training data")
# centers = generateCenters(k, x)
# sigma = generateSigmas(centers, k)
# weights = generateWeights(k)
# radials = findParams(x)[0]
# for q in range(1, k + 1):
#     plt.plot(x, [radial[q - 1] * weights[q] for radial in radials], 'r')
# x, y = readData("test.txt")
# plt.scatter(x, y, s=1, c='b', label="Test data")
# learn = False
# plt.plot(x, findParams(x), label="Final result")
# plt.legend()
# plt.grid()
# plt.savefig("point2_optimalSigma")

# PART 3

k = 11
learn = True
midDraw = False
x, y = readData("data.txt")
for k in range(1, 42, 5):
    error = []
    for i in range(100):
        centers = generateCenters(k, x)
        sigma = random.uniform(1.3, 1.6) if k == 1 else generateSigmas(centers, k)
        weights = generateWeights(k)
        error.append((findParams(x)[1])[-1])
    meanError = (sum(error) / len(error))
    stdDev = stdDeviation(meanError, error)
    with open("point3.txt", "a+") as f:
        f.write("No of neurons = " + str(k) + '\n')
        f.write("Averge error = " + str(meanError) + '\n')
        f.write("Standar deviation = " + str(stdDev) + '\n')

# PART 4
# k = 11
# plt.clf()
# plt.title("Output from linear layer during the learning process")
# midDraw = True
# learn = True
# x, y = readData("data.txt")
# plt.scatter(x, y, s=1, c='g', label="Training data")
# centers = generateCenters(k, x)
# sigma = generateSigmas(centers, k)
# weights = generateWeights(k)
# findParams(x)
# plt.grid()
# plt.legend()
# plt.savefig("point4")