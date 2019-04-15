import sys
from neuron import Neuron
import numpy as np
import matplotlib.pyplot as plt




# 0.1 0.1
# 0.5 0.5 
# 0.9 0.9

def stdDeviation(mean, x):
    sum = 0
    for i in x:
        sum += (i - mean)**2

    return sum / (len(x) - 1)

err = []
epoch = []
for i in range(100):
    x = Neuron(sys.argv[1], 1000000, 2)
    x.stop = True
    x.alpha = 0.9
    x.momentum = 0.9
    a = x.run()
    err.append(a[1])
    epoch.append(a[0])

avgErr = sum(err) / len(err)
avgEpoch = sum(epoch) / len(epoch)
print("Error avg: %s" % avgErr)
print("Epoch avg: %s" % avgEpoch)
stdDev = stdDeviation(avgErr, err)
with open("third", 'a+') as f:
    f.write("Alpha = %s\n" % x.alpha)
    f.write("Momentum = %s\n" % x.momentum)
    f.write("Average error = %s\n" % avgErr)
    f.write("Average epoch = %s\n" % avgEpoch)
    f.write("Standard deviation = %s\n" % stdDev)

        
err = []
epoch = []
for i in range(100):
    x = Neuron(sys.argv[1], 1000000, 2)
    x.stop = True
    x.alpha = 0.1
    x.momentum = 0.1
    a = x.run()
    err.append(a[1])
    epoch.append(a[0])

avgErr = sum(err) / len(err)
avgEpoch = sum(epoch) / len(epoch)
print("Error avg: %s" % avgErr)
print("Epoch avg: %s" % avgEpoch)
stdDev = stdDeviation(avgErr, err)
with open("third", 'a+') as f:
    f.write("Alpha = %s\n" % x.alpha)
    f.write("Momentum = %s\n" % x.momentum)
    f.write("Average error = %s\n" % avgErr)
    f.write("Average epoch = %s\n" % avgEpoch)
    f.write("Standard deviation = %s\n" % stdDev)

err = []
epoch = []
for i in range(100):
    x = Neuron(sys.argv[1], 1000000, 2)
    x.stop = True
    x.alpha = 0.5
    x.momentum = 0.5
    a = x.run()
    err.append(a[1])
    epoch.append(a[0])

avgErr = sum(err) / len(err)
avgEpoch = sum(epoch) / len(epoch)
stdDev = stdDeviation(avgErr, err)
with open("third", 'a+') as f:
    f.write("Alpha = %s\n" % x.alpha)
    f.write("Momentum = %s\n" % x.momentum)
    f.write("Average error = %s\n" % avgErr)
    f.write("Average epoch = %s\n" % avgEpoch)
    f.write("Standard deviation = %s\n" % stdDev)


err = []
epoch = []
for i in range(100):
    x = Neuron(sys.argv[1], 1000000, 2)
    x.stop = True
    x.alpha = 0.2
    x.momentum = 0.5
    a = x.run()
    err.append(a[1])
    epoch.append(a[0])

avgErr = sum(err) / len(err)
avgEpoch = sum(epoch) / len(epoch)
print("Error avg: %s" % avgErr)
print("Epoch avg: %s" % avgEpoch)
stdDev = stdDeviation(avgErr, err)
with open("third", 'a+') as f:
    f.write("Alpha = %s\n" % x.alpha)
    f.write("Momentum = %s\n" % x.momentum)
    f.write("Average error = %s\n" % avgErr)
    f.write("Average epoch = %s\n" % avgEpoch)
    f.write("Standard deviation = %s\n" % stdDev)
