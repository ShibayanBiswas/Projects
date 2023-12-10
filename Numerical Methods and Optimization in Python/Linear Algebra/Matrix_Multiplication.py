
def multiply(a, b):
    # we have to store the results in a matrix
    c = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]

    # iterate through the rows of matrix A
    for i in range(len(a)):
        # iterate through columns of B
        for j in range(len(b[0])):
            # iterate through rows of B
            for k in range(len(b)):
                c[i][j] += a[i][k] * b[k][j]

    return c


if __name__ == '__main__':
    print(multiply([[1, 2], [3, 4]], [[1, 2], [2, 1]]))