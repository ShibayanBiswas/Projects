from scipy.special import legendre
import matplotlib.pyplot as plt
import numpy as np

min = -1.0
max = 1.0
step = 0.05

p_n = legendre(1)
x = np.arange(min, max + step, step)
y = p_n(x)
plt.plot(x, y, label='$P_1$')

p_n = legendre(2)
x = np.arange(min, max + step, step)
y = p_n(x)
plt.plot(x, y, label='$P_2$')

p_n = legendre(3)
x = np.arange(min, max + step, step)
y = p_n(x)
plt.plot(x, y, label='$P_3$')

p_n = legendre(4)
x = np.arange(min, max + step, step)
y = p_n(x)
plt.plot(x, y, label='$P_4$')

p_n = legendre(5)
x = np.arange(min, max + step, step)
y = p_n(x)
plt.plot(x, y, label='$P_5$')

plt.title("Plot of the first five Legendre Polynomials")
plt.xlabel("X- axis")
plt.ylabel("Y- axis")
plt.grid()
plt.legend()
plt.show()
