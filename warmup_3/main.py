import sys
from random import random
import math
import numpy as np

if (len(sys.argv) < 3):
    print("Usage: python main.py <input file> <mode>")
    exit()

typ = sys.argv[2]

def inFile():
    file = open(sys.argv[1])
    f = file.readlines()
    x = []
    y = []
    for i in f:
        x.append(float((i.split(';'))[0]))
        y.append(float((i.split(';'))[1].strip('\n')))
    return x,y


def cost_offLine(v, e):
    sum = 0
    for i in range(0, len(y)):
        sum += (v[i] - e[i])**2
    
    return (sum/(2*len(v)))

def cost_onLine(v, e):
    return ((v - e)**2)/2


def sigmoid(x):
    return 1/(1-math.exp(-x))

def derivative_sigmoid(x):
    y = sigmoid(x)
    return y*(1-y)

def calcB2(x, expected, a):
    return (x - expected)*derivative_sigmoid(a)

def calcB1(weight, a, b2):
    return b2 * weight * derivative_sigmoid(a)


w1 = np.array([[random(), random()], [random(), random()]])
w2 = [random(), random(), random()]
eps = 0.01




