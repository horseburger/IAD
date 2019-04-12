import sys
from neuron import Neuron



x = Neuron(sys.argv[1], sys.argv[2], 2)
print(x.w1, x.w2)
a = x.run()
y = Neuron(sys.argv[1], sys.argv[2], 2)
y.w1 = x.w1
y.w2 = x.w2
y.bias = False
b = y.run()

with open('first.txt', 'w') as f:
    for x in a[2]:
        f.write("%s\n" % x)
    f.write("#############\n")
    for x in a[3]:
        f.write("%s\n" % x)
with open('second.txt', 'w') as f:
    for x in b[2]:
        f.write("%s\n" % x)
    f.write("#############\n")
    for x in b[3]:
        f.write("%s\n" % x)
