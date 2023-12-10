import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[1, 2], [2, 1]])

c = np.matmul(a, b)
print(c)

# inner product (vector-vector multiplication)
v1 = np.array([1, 2, 3])
v2 = np.array([2, 3, 4])

print(np.dot(v1, v2))