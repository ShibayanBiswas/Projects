import numpy as np
from matplotlib import pyplot as plt


def f(g, l, x, b, v):
    return (-g/l)*x-b*v


def runge_kutta_method(x=0, v=1, g=9.8, l=1, dt=0.1, b=0.3):
    x_values = []
    t_values = []
    t = 0

    while t < 100:
        x_values.append(x)
        t_values.append(t)

        k1 = dt * f(g, l, x, b, v)
        k2 = dt * f(g, l, x, b, v + dt * k1 / 2)
        k3 = dt * f(g, l, x, b, v + dt * k2 / 2)
        k4 = dt * f(g, l, x, b, v + dt * k3)

        v = v + 1.0 / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        x = x + v*dt
        t = t + dt

    plt.plot(t_values, x_values)
    plt.show()


if __name__ == '__main__':
    runge_kutta_method()