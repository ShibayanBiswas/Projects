import numpy as np


def f(x):
    return x * x * x


class MonteCarloIntegration:

    def __init__(self, a, b, n=100):
        self.a = a
        self.b = b
        self.n = n

    def run(self):
        # area under the f(x) function
        s = 0

        for _ in range(self.n):
            random_x = self.generate_random()
            s += f(random_x) * (self.b - self.a)

        return s / self.n

    # this is how we can generate a random float in the range [a,b]
    def generate_random(self):
        return self.a + (self.b-self.a)*np.random.uniform()


if __name__ == '__main__':
    algorithm = MonteCarloIntegration(0, 5, 10000000)
    print(algorithm.run())
