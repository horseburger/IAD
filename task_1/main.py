import sys
from neuron import Neuron



x = Neuron(sys.argv[1], sys.argv[2], 2)
x.run()

