import matplotlib.pyplot as plt
import numpy as np


def sin(min, max, num):
    x = np.linspace(min, max, num)
    y = np.sin(x)

    return x, y


def plot(func, *args):
    x, y = func(*args)

    plt.plot(x, y)
    plt.show()


plot(sin, 0, 4*np.pi, 1000)
