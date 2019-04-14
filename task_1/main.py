import sys
from neuron import Neuron
import numpy as np
import matplotlib.pyplot as plt

x = Neuron(sys.argv[1], sys.argv[2], 2)
y = Neuron(sys.argv[1], sys.argv[2], 2)
y.w1 = x.w1
y.w2 = x.w2
y.bias = False
# a = x.run()
b = y.run()




# with open('bias', 'w') as f:
#     for i in a[2]:
#         f.write("%s\n" % i)
#     f.write("################\n")
#     for i in a[3]:
#         f.write("%s\n" % i)
with open('no_bias', 'w') as f:
    for i in b[2]:
        f.write("%s\n" % i)
    f.write("################\n")
    for i in b[3]:
        f.write("%s\n" % i)

# ta = [i for i in range(len(a[2]))]
tb = [i for i in range(len(b[2]))]

# plt.clf()
# plt.plot(ta, a[2], 'o')
# plt.plot(ta, a[3], 'ro')
# plt.savefig('first')
plt.clf()
plt.plot(tb, b[2], 'o')
plt.plot(tb, b[3], 'ro')
plt.savefig('second')
