import matplotlib.pyplot as plt
import numpy as np
import random

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

def calculateError(f, y):
    sum = 0
    for i in range(len(f)):
        sum += (f[i] - y[i])**2
    return sum / 2*len(f)

def partialDerivative(f, y, z):
    sum = 0
    for i in range(len(f)):
        sum += (f[i] - y[i]) * z
    return sum / len(f)
