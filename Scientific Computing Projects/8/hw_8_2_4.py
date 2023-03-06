import matplotlib.pyplot as plt
import numpy as np
import statistics as st
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq, ifft

file_path = r"C:\Users\shiba\Downloads\noise.inp"
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

new_signal = list()

for i in range(0,996):
    new_signal.append(st.median((signal[i : (i + 4)])))

new_yf = fft(new_signal)
new_xf = fftfreq(996, 0.0001)

plt.plot(new_xf, np.abs(new_yf), label = ' FFT of the Average Time Signal', linewidth = 0.5)
plt.title('Plot of FFT of the Average Time Signal')
plt.xlabel('Frequency')
plt.ylabel('Fast Fourier Transform')
plt.grid()
plt.legend(loc = 'upper right')
plt.show()
