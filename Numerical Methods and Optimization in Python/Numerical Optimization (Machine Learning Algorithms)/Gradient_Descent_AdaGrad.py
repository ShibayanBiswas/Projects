import numpy as np


# cost-function
def f(x, y):
    return x * x + y * y + 3


# derivative of the cost-function
def df(x, y):
    return np.asarray([2.0 * x, 2.0 * y])


# gradient descent algorithm with AdaGrad
# [[-1, 1], [-1, 1]]
def adaptive_gradient(bounds, n, alpha, epsilon=1e-8):
    # generate an initial point
    solution = np.asarray([0.7, 0.8])
    # G values (sum of the squared past gradients)
    # we have 1 value for every feature (x and y in this case)
    # the value is the sum of the past squared gradients in every iteration
    g_sums = [0.0 for _ in range(bounds.shape[0])]

    # run the gradient descent
    for _ in range(n):
        # calculate gradients
        gradient = df(solution[0], solution[1])

        # update the sum of the squared gradients for all the features
        # (x and y in this case)
        for i in range(gradient.shape[0]):
            g_sums[i] += gradient[i] ** 2.0

        # build a solution one variable at a time
        new_solution = []

        # we consider all the features - as we use different learning rates
        for i in range(solution.shape[0]):
            # calculate the step size for that feature
            adaptive_alpha = alpha / (np.sqrt(g_sums[i]) + epsilon)
            new_solution.append(solution[i] - adaptive_alpha * gradient[i])

        solution = np.asarray(new_solution)
        solution_value = f(solution[0], solution[1])
        print('(%s) - function value: %s' % (solution, solution_value))


if __name__ == '__main__':
    adaptive_gradient(np.asarray([[-1.0, 1.0], [-1.0, 1.0]]), 200, 0.1)