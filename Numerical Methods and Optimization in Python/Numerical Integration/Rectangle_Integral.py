def f(x):
    return x * x


def rectangle_integral(a, b, n=1000000):
    # width of a single rectangle
    h = (b - a) / n
    # sum of the integral (area under the f(x) function)
    s = 0

    # we sum up the areas of the single rectangles
    for i in range(n):
        s += h * f(a + i * h)

    return s


if __name__ == '__main__':
    print(rectangle_integral(0, 1))

