import sys
from random import random
from random import shuffle
from random import seed
import numpy as np
import matplotlib.pyplot as plt
# import bigfloat

if (len(sys.argv) < 3):
    print("Usage: python main.py <input file> <mode>\nOn-line - 0\nOff-line - 1")
    exit()

typ = sys.argv[2]
alpha = 0.1
eps = 0.0001
it = 10000


def inFile():
    file = open(sys.argv[1])
    f = file.readlines()
    x = []
    y = []
    for i in f:
        x.append(float((i.split(';'))[0]))
        y.append(float((i.split(';'))[1].strip('\n')))

    return (x, y)

def saveGraph(filename, y):
    plt.clf()
    x = list(range(len(y)))
    plt.plot(x, y, 'r')
    plt.savefig(filename)

def saveRightGraph(filename, w):
    plt.clf()
    plt.axis([-3, 5, -0.5, 1.2])

    x = np.arange(-3., 6., 0.1)

    plt.plot(x, offLine_findParams(x, 0, w[0], w[1], w[2], 1))
    plt.savefig(filename)




def saveErrorGraph(filename, error):

    x = []
    for i in range(len(error)):
        x.append(i)

    plt.clf()
    plt.axis([0, len(error), 0, 0.4])
    plt.plot(x, error)
    plt.savefig(filename)



def sigmoid(x):
    return 1/(1 + np.exp(-x))

def derivative_sigmoid(x):
    y = sigmoid(x)
    return y*(1-y)

def calcA(x, w):
    sum = 0
    x_withBias = [1]
    if type(x) == list: x_withBias.extend(x)
    else: x_withBias.append(x)
    for i in range(len(x_withBias)):
        sum += x_withBias[i] * w[i]

    return sum

def offLine_calcTopB(a, y):
    return (sigmoid(a) - y) * derivative_sigmoid(a)

def offLine_calcLowB(b, w, a):
    return b * w * derivative_sigmoid(a)

def offLine_calcError(b, x):
    sum = 0

    for i in range(len(b)):
        sum += b[i] * x[i]

    return sum / len(b)

def offLine_cost(result, y):
    sum = 0

    for i in range(len(result)):
        sum += (result[i] - y[i])**2

    return sum / (2*len(y))

def offLine_findParams(x, y, w11, w12, w2, mode):

    
    oneVec = [1 for i in range(len(x))]
    error = []
    for j in range(it):

        y11 = []
        y12 = []
        y2 = []
        a11 = []
        a12 = []
        a2 = []

        b11 = []
        b12 = []
        b2 = []

        result = []
        
        
        for i in range(len(x)):
            a11.append(calcA(x[i], w11))
            a12.append(calcA(x[i], w12))

            y11.append(sigmoid(a11[-1]))
            y12.append(sigmoid(a12[-1]))

            a2.append(calcA([y11[-1], y12[-1]], w2))

            y2.append(sigmoid(a2[-1]))
            result.append(y2[-1])

        if mode:
            return result

        if j == 0:
            saveGraph("wrong.png", result)
        
        error.append(offLine_cost(result, y))
        print(error[-1])

        for i in range(len(y)):
            b2.append(offLine_calcTopB(a2[i], y[i]))

        chng1 = offLine_calcError(b2, oneVec)
        chng2 = offLine_calcError(b2, y11)
        chng3 = offLine_calcError(b2, y12)

        # if chng1 < eps or chng2 < eps or chng3 < eps:
            # break

        w2[0] -= alpha * chng1
        w2[1] -= alpha * chng2
        w2[2] -= alpha * chng3

        for i in range(len(y)):
            b11.append(offLine_calcLowB(b2[i], w2[1], a11[i]))
            b12.append(offLine_calcLowB(b2[i], w2[2], a12[i]))

        chng1 = offLine_calcError(b11, oneVec)
        chng2 = offLine_calcError(b11, x)
        chng3 = offLine_calcError(b12, oneVec)
        chng4 = offLine_calcError(b12, x)

        # if chng1 < eps or chng2 < eps or chng3 < eps or chng4 < eps:
            # break

        w11[0] -= alpha * chng1
        w11[1] -= alpha * chng2
        w12[0] -= alpha * chng3
        w12[1] -= alpha * chng4
        

        s = random()
        seed(s)
        shuffle(x)
        seed(s)
        shuffle(y)
        
        
        
        
    saveErrorGraph("error.png", error)



    return w11, w12, w2


# # # # # # # # # # # # # # 

def onLine_calcError(b, x):
    return b * x

def onLine_cost(result, y):
    return ((result - y)**2) / 2

def onLine_findParams(x, y, w11, w12, w2, mode):

    
    oneVec = [1 for i in range(len(x))]
    error = []
    for j in range(it):
        y11 = 0
        y12 = 0
        y2 = 0
        a11 = 0
        a12 = 0
        a2 = 0

        b11 = 0
        b12 = 0
        b2 = 0

        result = []
        
        
        for i in range(len(x)):
            a11 = calcA(x[i], w11)
            a12 = calcA(x[i], w12)

            y11 = sigmoid(a11)
            y12 = sigmoid(a12)

            a2 = calcA([y11, y12], w2)

            y2 = sigmoid(a2)
            result.append(y2)

            error.append(onLine_cost(result[i], y[i]))
            print(error[-1])

            b2 = offLine_calcTopB(a2, y[i])


            w2[0] -= alpha * onLine_calcError(b2, 1)
            w2[1] -= alpha * onLine_calcError(b2, y11)
            w2[2] -= alpha * onLine_calcError(b2, y12)

            if np.all(np.abs(w2) < eps):
                break

            b11 = offLine_calcLowB(b2, w2[1], a11)
            b12 = offLine_calcLowB(b2, w2[2], a12)

            w11[0] -= alpha * onLine_calcError(b11, 1)
            w11[1] -= alpha * onLine_calcError(b11, x[i])
            w12[0] -= alpha * onLine_calcError(b12, 1)
            w12[1] -= alpha * onLine_calcError(b12, x[i])


            if np.all(np.abs(w11) < eps) or np.all(np.abs(w12) < eps):
                break


        if mode:
            return result

        if j == 0:
            saveGraph("wrong.png", result)

        

        s = random()
        seed(s)
        shuffle(x)
        seed(s)
        shuffle(y)

    saveErrorGraph("error_onLine.png", error)
    return w11, w12, w2

# POPRAWNE WAGI 
# [[-13.87918584   6.83788511]
# [  7.70402616 -14.47464708]]
# [[  7.04136624 -13.34467331 -15.97262107]]

####################################################

data = inFile()
w11 = [random(), random()]
w12 = [random(), random()]
w2 = [random(), random(), random()]

# w11 = [-13.87918584, 6.83788511]
# w12 = [7.70402616, -14.47464708]
# w2 = [ 7.04136624, -13.34467331, -15.97262107]
if typ == '1':
    w11, w12, w2 = offLine_findParams(data[0], data[1], w11, w12, w2, 0)
else:
    w11, w12, w2 = onLine_findParams(data[0], data[1], w11, w12, w2, 0)

saveRightGraph("right.png", [w11, w12, w2])