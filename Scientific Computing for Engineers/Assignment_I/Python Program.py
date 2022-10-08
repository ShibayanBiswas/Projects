import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-3, 3, 100)
    y = np.exp(x)
    plt.figure()
    plt.plot(x, y)
    plt.plot(x, -np.exp(-x))
    plt.title('exp(x) & -exp(x)')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()
