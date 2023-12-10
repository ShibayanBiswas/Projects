
def f(x):
    return x * x


def integral(a, b, n=1000):
    h = (b - a) / n
    s = 0

    # evaluate the function at f(a) and f(b)
    s += f(a) + f(b)

    # consider the internal points with 4 as the constant (every second point)
    for i in range(1, n, 2):
        s += 4 * f(a + i * h)

    # consider the internal points with 2 as the constant (every second point)
    for i in range(2, n, 2):
        s += 2 * f(a + i * h)

    return h * s / 3


if __name__ == '__main__':
    print(integral(0, 1))

