import sys
import numpy as np
import random


def f(x, w):
    return 1/(1+np.exp(-(float(x)*float(w[1]) + float(w[0]))))


def error(x, y, w):

    err = 0
    for i in range(0, len(x)):
        err += ((f(float(x[i])-float(y[i]), w)))**2

    return err/2*len(x)

def derivative(x, y, w):
    res = 0
    for i in range(0, len(x)):
        res += (f(x[i], w) - float(y[i]) * (f(x[i], w) * (1 - f(x[i], w)) * float(x[i])))

    return res/len(x)


fr = open("in.txt", 'r')
fw = open("out.txt", 'w')

# x = np.arange(-1., -1., 0.1)
w = [random.uniform(-1, 1), random.uniform(-1, 1)]

fread = fr.readlines()
fread = [s.replace('\n', '') for s in fread]

x = []
y = []

for s in fread:
    x.append(s.split(';')[0])
    y.append(s.split(';')[1])


# w(t) to poprzednia iteracja 
