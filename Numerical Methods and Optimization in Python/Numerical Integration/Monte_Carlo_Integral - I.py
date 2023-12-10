import numpy as np


def f(x):
    return x * x * x


class MonteCarloIntegration:

    def __init__(self, a, b, n=100):
        self.a = a
        self.b = b
        self.n = n

    def run(self):
        # count the number of generated points under f(x)
        counter = 0

        for _ in range(self.n):
            random_x = self.generate_random()
            random_y = self.generate_random()

            if self.is_below(random_x, random_y):
                counter += 1

        return self.get_total_area() * counter / self.n

    # the bounding box (THIS IS THE MAIN DISADVANTAGE !!!)
    # b-a defines the width (height) of the interval
    def get_total_area(self):
        return (self.b-self.a) * (self.b-self.a)

    # this is how we can generate a random float in the range [a,b]
    def generate_random(self):
        return self.a + (self.b-self.a)*np.random.uniform()

    # checks if the generated point is below the f(x) function or not
    @staticmethod
    def is_below(x, y):
        if y < f(x):
            return True

        return False


if __name__ == '__main__':
    algorithm = MonteCarloIntegration(0, 5, 1000000)
    print(algorithm.run())
