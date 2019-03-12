import matplotlib.pyplot as plt
import numpy as np

def f1(x):
    return 1/(1+np.exp(-x)) # red
def f2(x):
    return 1/(1+np.exp(4*x)) # blue
def f3(x):
    return 1/(1+np.exp(-100*x+55)) # green

x_val = [-0.2, 0.4, 0.5, 0.6, 1.2, 1.9]
y_val = [0, 0, 0, 1, 1, 1]
plt.axis([-3.0, 3.0, -0.5, 1.5])
x = np.arange(-3.0, 3.1, 0.1)
plt.plot(x, f1(x), 'r', x, f2(x), 'b', x, f3(x), 'g', linewidth=3)
plt.plot(x_val, y_val, 'ko')
plt.xlabel("Rozgrzewka 1")
plt.xticks(np.arange(min(x), max(x), 0.5))
plt.show()
