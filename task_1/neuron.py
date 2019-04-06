from random import random
from random import seed 
from random import shuffle
import numpy as np
import matplotlib.pyplot as plt

class Neuron:

    def __init__(self, filename, it, n):
        self.alpha = 0.1
        self.x = self.inFile(filename)
        # self.y = self.x
        self.it = int(it)
        self.momentum = 0
        self.bias = True
        self.eps = 0.0001
        self.number = n

        self.w1 = np.array([[random(), random(), random(), random(), random()]])
                #    [random(), random(), random(), random(), random()],
                #    [random(), random(), random(), random(), random()]])
        for i in range(self.number - 1):
            self.w1 = np.append(self.w1, [[random(), random(), random(), random(), random()]], axis=0)

        self.w2 = np.array([[random(), random(), random(), random()],
                   [random(), random(), random(), random()],
                   [random(), random(), random(), random()],
                   [random(), random(), random(), random()]])
    

    def cost(self, result, y):
        final = []
        for i in range(len(result)):
            final.append(((result[i] - y[i])**2) / 2)

        return final

    def calcError(self, b, x):
        return b * x

    def sigmoid(self, a):
        return 1 / (1 + np.exp(-a))

    def sigmoid_derivative(self, a):
        y = self.sigmoid(a)
        return y * (1 - y)

    def lowB(self, b, w, a):
        sum = 0
        for i in range(len(b)):
            sum += b[i] * w[i]
        
        return sum * self.sigmoid_derivative(a)
    
    def highB(self, a, y):
        return (self.sigmoid(a) - y) * self.sigmoid_derivative(a)

    def calcA(self, x, w):
        sum = 0
        if self.bias:
            x_withBias = [1]
        else:
            x_withBias = [0]
        if type(x) == list: x_withBias.extend(x)
        else: x_withBias.append(x)
        for i in range(len(x_withBias)):
            sum += x_withBias[i] * w[i]
        return sum

    def run(self):
        return self.findParams(3)

    def findParams(self, n):
        error = []
        oneVec = [1 for i in range(len(self.x))]
        flag = False

        for j in range(self.it):
            


            result = []


            for i in range(len(self.x)):
                y1 = []
                y2 = []


                a1 = []
                a2 = []

                b1 = []
                b2 = []

                for k in range(len(self.w1)):
                    a1.append(self.calcA(self.x[i], self.w1[k]))


                for k in range(len(a1)):
                    y1.append(self.sigmoid(a1[k]))

                for k in range(len(self.w2)):
                    a2.append(self.calcA(y1, self.w2[k]))

                for k in range(len(a2)):
                    y2.append(self.sigmoid(a2[k]))

                result.append(y2)

                error.append(self.cost(result[-1], self.x[i]))
                print(error[-1])

                for k in range(len(a2)):
                    b2.append(self.highB(a2[k], self.x[i][k]))


                c = [self.calcError(b2[0], 1)]
                for k in range(len(y1)):
                    c.append(self.calcError(b2[0], y1[k]))

                # if self.checkWeights(c):
                #     flag = True
                #     break

                for k in range(len(c)):
                    self.w2[0][k] -= self.alpha * c[k]
                
                c = [self.calcError(b2[1], 1)]
                for k in range(len(y1)):
                    c.append(self.calcError(b2[1], y1[k]))

                # if self.checkWeights(c):
                #     flag = True
                #     break
                
                for k in range(len(c)):
                    self.w2[1][k] -= self.alpha * c[k]

                c = [self.calcError(b2[2], 1)]
                for k in range(len(y1)):
                    c.append(self.calcError(b2[2], y1[k]))

                # if self.checkWeights(c):
                #     flag = True
                #     break

                for k in range(len(c)):
                    self.w2[2][k] -= self.alpha * c[k]

                c = [self.calcError(b2[3], 1)]
                for k in range(len(y1)):
                    c.append(self.calcError(b2[3], y1[k]))

                # if self.checkWeights(c):
                #     flag = True
                #     break
                
                for k in range(len(c)):
                    self.w2[3][k] -= self.alpha * c[k]

                for k in range(1, self.number + 1):
                    b1.append(self.lowB(b2, self.w2[k], a1[k - 1]))

                for k in range(len(b1)):
                    c = []
                    c.append(self.calcError(b1[k], 1))
                    c.append(self.calcError(b1[k], self.x[i][0]))
                    c.append(self.calcError(b1[k], self.x[i][1]))
                    c.append(self.calcError(b1[k], self.x[i][2]))


                    for l in range(len(c)):
                        self.w1[k][l] -= self.alpha * c[l]
                
                if flag:
                    break

                


            if flag:
                break
            
            shuffle(self.x)

        print("\nRESULTS:\n")
        for z in result:
            print(z)
        
            
        self.saveErrorPlot("error.png", error)
        return self.w1, self.w2


    def inFile(self, filename):
        file = open(filename)
        f = [ i.strip('\n') for i in file.readlines()]
        
        x = []
        
        for i in f:
            x.append(i.split(' '))

        for i in range(len(x)):
            for j in range(len(x[i])):
                x[i][j] = int(x[i][j])

        return x


        

    def saveErrorPlot(self, filename, error):
        plt.clf()

        x = []
        e1 = []
        e2 = []
        e3 = []
        e4 = []
        for i in range(len(error)):
            x.append(i)
            e1.append(error[i][0])
            e2.append(error[i][1])
            e3.append(error[i][2])
            e4.append(error[i][3])
        
        plt.axis([0, len(error), 0, 0.3])
        plt.plot(x, e1, 'r')
        plt.plot(x, e2, 'b')
        plt.plot(x, e3, 'g-')
        plt.plot(x, e4)
        plt.savefig(filename)