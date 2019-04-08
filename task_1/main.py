import sys
from neuron import Neuron



x = Neuron(sys.argv[1], sys.argv[2], 1)
x.run()
x = Neuron(sys.argv[1], sys.argv[2], 2)
x.run()
x = Neuron(sys.argv[1], sys.argv[2], 3)
x.run()
