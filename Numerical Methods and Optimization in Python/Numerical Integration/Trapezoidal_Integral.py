
def f(x):
    return x * x


def integral(a, b, n=10000):
    # h is the width of a single trapezoid
    h = (b-a)/n
    # sum of the areas of the trapezoids = integral
    s = 0

    # evaluate the function at f(a)
    s += f(a)

    # consider the internal points between a and b
    for i in range(1, n):
        s += 2 * f(a + i * h)

    # evaluate the function at f(b)
    s += f(b)

    return h * s / 2


if __name__ == '__main__':
    print(integral(0, 1))

