import numpy as np
import matplotlib.pyplot as plt

t = np.arange(-3., 4., 0.1)

plt.axis([-3,3,-0.5,1.5])

plt.plot([-0.2,0.4,0.6,1.2,1.9,0.5],[0,0,1,1,1,0], 'ko')
plt.plot(t, 1/(1+np.exp(-t)), 'r-')
plt.plot(t, 1/(1+np.exp(4*t)), 'b-')
plt.plot(t, 1/(1+np.exp(-100*t+55)), 'g-')
plt.show()