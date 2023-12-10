import numpy as np
from matplotlib import pyplot as plt

# dy/dx = x * y
# y(x) = exp(0.5 * x^2)
def f(x, y):
    return x * y

def range_kutta_method(x=0, y=1, dx=0.01):
    x_values = []
    y_values = []
    
    while x < 10:
        x_values.append(x)
        y_values.append(y)
        
        k1 = dx * f(x, y)
        k2 = dx * f(x + dx / 2, y + dx * k1 / 2)
        k3 = dx * f(x + dx / 2, y + dx * k2 / 2)
        k4 = dx * f(x + dx, y + dx * k3)
        
        y = y + 1.0 / 6.0 * (k1 + 2*k2 + 2*k3 + k4)
        x = x + dx
        
    plt.plot(x_values, y_values)
    plt.show()
    
if __name__ == '__main__':
    range_kutta_method()