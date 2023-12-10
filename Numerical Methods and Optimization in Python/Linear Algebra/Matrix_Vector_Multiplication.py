# 'a' is a matrix, 'b' is a vector
def multiply(a, b):
    # we have to store the results in a vector
    c = [0 for _ in range(len(b))]

    # iterate through the rows of the matrix
    for i in range(len(a)):
        # iterate through the vector
        for j in range(len(b)):
            c[i] += a[i][j] * b[j]

    return c


if __name__ == '__main__':
    print(multiply([[3, 2, 0], [0, 4, 1], [2, 0, 1]], [4, 3, 1]))