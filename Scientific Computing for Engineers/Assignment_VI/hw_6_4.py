import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.special import roots_legendre
from time import process_time
import math

def func(x):
    y = (math.exp(-x))*math.pow(math.sin(4*x),2)
    return y
correct_integral = quad(func, -1, 1)[0]

n = 9999  # Taking a very large value

target_error = [0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]

error = list()
y_list = list()
time = list()
index = 0

# Legendre Method
for i in range(1, n + 1):
    start = process_time()
    roots, weights = roots_legendre(i)
    calc_integral = 0
    for j in range(1, i + 1):
        calc_integral += func(roots[j-1])*weights[j-1]
    error.append(abs(correct_integral - calc_integral))
    if error[i - 1] < target_error[index]:
        y_list.append(i)
        index += 1
        end = process_time()
        time.append(end - start)
    if index == 6:
        break

# Trapezoid method
a = -1
b = 1
error_1 = list()
y_list_1 = list()
time_1 = list()
index = 0

for i in range(1, n + 1):
    start = process_time()
    dx = (b - a) / i
    calc_integral = func(a)+func(b)
    j = 1
    while j < i:
        calc_integral += 2 * func(a + j * dx)
        j += 1
    c_integral = (calc_integral * (dx / 2))
    error_1.append(abs(correct_integral - c_integral))
    if error_1[i - 1] < target_error[index]:
        y_list_1.append(i)
        index += 1
        end = process_time()
        time_1.append(end - start)
    if index == 6:
        break

plt.plot(target_error, time, label= 'Current (Legendre) Method')
plt.plot(target_error, time_1, label= 'Best (Trapezoid) Method')
plt.title('Plot of Computational Cost Required v/s Target Error Range')
plt.xlabel('Target Error Range')
plt.ylabel('Computational Cost Required')
plt.grid()
plt.legend()
plt.show()

