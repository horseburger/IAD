import sys
from neuron import Neuron
import numpy as np
import matplotlib.pyplot as plt

x = Neuron(sys.argv[1], sys.argv[2], 2)
print(x.w1, x.w2)
a = x.run()
y = Neuron(sys.argv[1], sys.argv[2], 2)
y.w1 = x.w1
y.w2 = x.w2
y.bias = False
b = y.run()

t = []

for i in range(len(a[2])):
    t.append(i)

plt.clf()
plt.plot(t, a[2], 'o')
plt.plot(t, a[3], 'ro')
plt.savefig('first')
plt.clf()
plt.plot(t, b[2], 'o')
plt.plot(t, b[3], 'ro')
plt.savefig('second')