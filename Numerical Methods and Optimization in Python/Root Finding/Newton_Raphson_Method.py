from math import sqrt


def f(x):
    return x * x - 2


def df(x):
    return 2 * x


def newton_method(x, n=10):
    counter = 0

    while counter < n:
        counter += 1
        x = x - f(x)/df(x)

    return x


if __name__ == '__main__':
    print(newton_method(1))
    print(sqrt(2))

