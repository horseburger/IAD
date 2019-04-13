import sys
from neuron import Neuron
import numpy as np
import matplotlib.pyplot as plt

x = Neuron(sys.argv[1], sys.argv[2], 2)
a = x.run()
y = Neuron(sys.argv[1], sys.argv[2], 2)
y.w1 = x.w1
y.w2 = x.w2
y.bias = False
b = y.run()

"""
run() returns w1, w2, and two tuples: results for the first neuron in the hidden layer and the second neuron
the tuple looks like: ([x], result)

"""


with open('bias', 'w') as f:
    for i in a[2]:
        f.write("%s -> %s\n" % (i[1], i[0]))
    f.write("################\n")
    for i in a[3]:
        f.write("%s -> %s\n" % (i[1], i[0]))
# with open('no_bias', 'w') as f:
#     for i in b[2]:
#         f.write("%s -> %s\n" %(b[2][1], b[2][0]))
#     f.write("################\n")
#     for i in b[3]:
#         f.write("%s -> %s\n" % (b[3][1], b[3][0]))


# plt.clf()
# plt.plot(t, c, 'o')
# plt.plot(t, a[3], 'ro')
# plt.savefig('first')
# plt.clf()
# plt.plot(t, b[2], 'o')
# plt.plot(t, b[3], 'ro')
# plt.savefig('second')
