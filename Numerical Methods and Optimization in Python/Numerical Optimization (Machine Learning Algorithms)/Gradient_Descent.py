from numpy import arange
import numpy as np
from matplotlib import pyplot as plt


# this is the cost-function
def f(x):
    return x * x


# derivative of the cost-function
def df(x):
    return 2 * x


# gradient descent algorithm - n is the number of iterations
# and alpha is the learning rate
def gradient_descent(start, end, n, alpha):
    # we track the results (x and f(x) values as well)
    x_values = []
    y_values = []
    # generate the initial starting point (random value)
    x = np.random.uniform(start, end)
    # we make n iterations
    for i in range(n):
        # this is the gradient descent formula (based on the derivative)
        x = x - alpha * df(x)
        # we store x and f(x) values
        x_values.append(x)
        y_values.append(f(x))
        print('#%d f(%s) - %s' % (i, x, f(x)))

    return [x_values, y_values]


if __name__ == '__main__':
    # perform the gradient descent search
    solutions, scores = gradient_descent(-1, 1, 50, 0.1)
    # sample input range uniformly at 0.1 increments to plot the function
    inputs = arange(-1, 1.1, 0.1)
    # create a line plot of input vs result
    plt.plot(inputs, f(inputs))
    # this is how we plot the steps of the algorithm
    plt.plot(solutions, scores, '.-', color='green')
    plt.show()