import numpy as np
from numpy import linalg as la

m = np.array([[2, 0], [0, 5]])
w, v = la.eig(m)
print(w)
print(v)