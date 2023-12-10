import numpy as np


# cost-function
def f(x, y):
    return x * x + y * y


# derivative of the cost-function
def df(x, y):
    return np.asarray([2.0 * x, 2.0 * y])


def adam(bounds, n, alpha, beta1, beta2, epsilon=1e-8):
    # generate an initial point (random usually)
    x = np.asarray([0.8, 0.9])
    # initialize first moment and second moment
    m = [0.0 for _ in range(bounds.shape[0])]
    v = [0.0 for _ in range(bounds.shape[0])]

    for t in range(1, n+1):
        # gradient g(t) so the partial derivatives
        g = df(x[0], x[1])
        # update every feature independently
        for i in range(x.shape[0]):
            m[i] = beta1 * m[i] + (1.0 - beta1) * g[i]
            v[i] = beta2 * v[i] + (1.0 - beta2) * g[i] ** 2
            m_corrected = m[i] / (1.0 - beta1 ** t)
            v_corrected = v[i] / (1.0 - beta2 ** t)
            x[i] = x[i] - alpha * m_corrected / (np.sqrt(v_corrected) + epsilon)

        print('(%s) - function value: %s' % (x, f(x[0], x[1])))


if __name__ == '__main__':
    adam(np.asarray([[-1.0, 1.0], [-1.0, 1.0]]), 100, 0.05, 0.9, 0.999)
