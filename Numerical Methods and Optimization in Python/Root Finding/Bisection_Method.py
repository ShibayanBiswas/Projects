from math import sqrt


def f(x):
    return x * x - 2


def bisection_method(x_neg, x_pos, eps=1e-10):
    x = 0

    while abs(x_pos - x_neg) > eps:
        x = (x_pos + x_neg) / 2

        if f(x) > 0:
            x_pos = x
        else:
            x_neg = x

    return x


if __name__ == '__main__':
    print(bisection_method(-2, 2))
    print(sqrt(2))
