import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.special import roots_legendre
import math

def func(x):
    y = (math.exp(-x))*math.pow(math.sin(4*x),2)
    return y
correct_integral = quad(func, -1, 1)[0]

n = 9999  # Taking a very large value

target_error = [0.1, 0.01, 0.001, 0.0001]

roots, weights = roots_legendre(n)

error = list()
y_list = list()
index = 0

# Legendre Method
for i in range(1, n + 1):
    calc_integral = 0
    for j in range(1, i + 1):
        calc_integral += func(roots[j-1])*weights[j-1]
    error.append(abs(correct_integral - calc_integral))

for i in range(0, len(error)):
    if error[i] < target_error[index]:
        y_list.append(i + 1)
        index += 1
    if index == 4:
        break

# Trapezoid Method
a = -1
b = 1
error_1 = list()
y_list_1 = list()
index = 0

for i in range(1, n + 1):
    dx = (b - a) / n
    calc_integral = func(a)+func(b)
    for j in range(1, i):
        const = a + j * dx
        calc_integral += 2 * func(const)
    calc_integral *= dx / 2
    error_1.append(abs(correct_integral - calc_integral))

for i in range(0, len(error_1)):
    if error_1[i] < target_error[index]:
        y_list_1.append(i + 1)
        index += 1
    if index == 4:
        break
        
plt.plot(target_error, y_list, label= 'Current (Legendre) Method')
plt.plot(target_error, y_list_1, label= 'Best (Trapezoid) Method')
plt.title('Plot of Number of Quadrature Points Required v/s Target Error Range')
plt.xlabel('Target Error Range')
plt.ylabel('Number of Quadrature Points Required')
plt.grid()
plt.legend()
plt.show()
     
