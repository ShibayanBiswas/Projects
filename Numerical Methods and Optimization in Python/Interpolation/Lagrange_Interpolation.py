import numpy as np
import matplotlib.pyplot as plt


class LagrangeInterpolation:

    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        self.b = None
        self.m = [[0 for _ in range(n+1)] for _ in range(len(x))]

    def plot(self):
        plt.scatter(self.x, self.y)

        x = np.linspace(-3, 3, 100)
        fx = 0

        for i in range(len(self.b)):
            fx += self.b[i] * x ** i

        plt.plot(x, fx)
        plt.show()

    def solve(self):
        # set matrix first column to be 1
        for i in range(len(self.x)):
            self.m[i][0] = 1

        # other columns of the matrix are the powers of x
        for i in range(1, self.n+1):
            for j in range(len(self.x)):
                self.m[j][i] = pow(self.x[j], i)

        # transform the list into a NumPy array and
        # calculating the final matrix we will use
        self.m = np.array(self.m)
        self.b = self.m.transpose().dot(self.y)
        self.m = np.matmul(self.m.transpose(), self.m)

        # solve the linear system with Gaussian elimination
        self.gaussian_elimination()
        print('Result of interpolation: %s' % self.b)

    def gaussian_elimination(self):
        n = len(self.b)
        # set all the values under the diagonal to be zeros
        # k runs from 0 to n-1 (so it considers all the columns)
        for k in range(n - 1):
            # we have to set all the values below the pivot row to be zero
            for i in range(k + 1, n):
                if self.m[i, k] != 0.0:
                    # this is how we determine the value that will make the actual value 0
                    lam = self.m[i, k] / self.m[k, k]
                    self.m[i, k:n] = self.m[i, k:n] - lam * self.m[k, k:n]
                    self.b[i] = self.b[i] - lam * self.b[k]

        # back substitution
        for k in range(n - 1, -1, -1):
            self.b[k] = (self.b[k] - np.dot(self.m[k, k + 1:n], self.b[k + 1:n])) / self.m[k, k]


if __name__ == '__main__':
    algorithm = LagrangeInterpolation([-2, -1, 0, 1, 2], [5.1, 1.9, 1.1, 2.1, 4.9], 2)
    algorithm.solve()
    algorithm.plot()

