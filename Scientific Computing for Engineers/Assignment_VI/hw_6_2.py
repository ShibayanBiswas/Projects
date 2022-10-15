import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.special import roots_legendre
import math

def func(x):
    y = (math.exp(-x))*math.pow(math.sin(4*x),2)
    return y
correct_integral = quad(func, -1, 1)[0]

n = int(input("Enter the number of terms in the series : "))

roots, weights = roots_legendre(n)
log_error = list()
for i in range(1, n + 1):
    calc_integral = 0
    for j in range(1, i + 1):
        calc_integral += func(roots[j-1])*weights[j-1]
    log_error.append(math.log(abs(correct_integral - calc_integral)))
x_list = list()
for i in range(1, n + 1):
    x_list.append(i)

plt.plot(x_list, log_error,label='log(error) v/s N')
plt.title('Plot of  Logarithm of Error v/s number of terms in the series (N) ')
plt.xlabel('number of terms in the series (N) ')
plt.ylabel('Logarithm of Error')
plt.grid()
plt.legend()
plt.show()
    
