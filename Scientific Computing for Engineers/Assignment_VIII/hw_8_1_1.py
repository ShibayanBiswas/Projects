import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq

file_path = r"C:\Users\shiba\Downloads\signal.inp"
file = np.loadtxt(file_path, delimiter = ' ', dtype = 'float')

time = list()
signal = list()

for i in range(len(file)):
    # Extracting time values
    x = file[i,0]
    time.append(x)
    # Extracting signal values
    y = file[i,1]
    signal.append(y)

yf = fft(signal)/1000
# xf = fftfreq(Number of Samples, ((time[999] - time[0])/(Number of Samples)))
xf = fftfreq(1000, 0.0001)

plt.plot(xf, np.abs(yf), label = 'Amplitude v/s Frequency', linewidth = 0.5)
plt.title('Plot of Amplitude v/s Frequency for the given Signal')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.grid()
plt.legend(loc = 'upper right')
plt.show()



