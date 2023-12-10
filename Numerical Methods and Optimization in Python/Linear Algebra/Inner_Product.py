# 'a' is a vector, 'b' is a vector
def multiply(a, b):
    # we have to store the results in a scalar
    c = 0

    for i in range(len(a)):
        c += a[i] * b[i]

    return c


def multiply_python(a, b):
    return sum([i*j for (i, j) in zip(a, b)])


if __name__ == '__main__':
    print(multiply([1, 2, 4, 5], [2, 5, 4, 5]))
    print(multiply_python([1, 2, 4, 5], [2, 5, 4, 5]))