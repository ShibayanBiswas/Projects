import numpy as np
from matplotlib import pyplot as plt


# dy/dx = cos(x)   y=sin(x)
def f(x, y):
    return np.cos(x)


# this is the initial condition y(0)=1
def euler_method(x=0, y=1, h=0.01):
    x_values = []
    y_values = []

    while x < 10:
        x_values.append(x)
        y_values.append(y)
        y = y + h * f(x, y)
        x = x + h

    plt.plot(x_values, y_values)
    plt.show()


if __name__ == '__main__':
    euler_method()
