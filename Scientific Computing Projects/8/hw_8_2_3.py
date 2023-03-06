import matplotlib.pyplot as plt
import numpy as np
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

yf = fft(signal)/1000
# xf = fftfreq(Number of Samples, ((time[999] - time[0])/(Number of Samples)))
xf = fftfreq(1000, 0.0001)

max_f = list()  # Frequency values at peaks
max_a = list()  # Amplitude values at peaks

pos = list()

for i in range(0, 999):
    if yf[i] > 0.01:
        pos.append(i)

# Temporary initialisation
time_1 = time

for i in pos:
    # Remove Amplitudes corresponding to True Frequencies
    yf = np.delete(yf, i)
    # Removing True Frequencies
    xf = np.delete(xf, i)
    # Removing Time Values corresponding to True Frequencies
    time_1 = np.delete(time_1, i)

# Calculating Signal Values for updated Amplitude Values
signal_1 = np.abs(ifft(yf*1000))

plt.subplot(2, 1, 1)
plt.plot(time, signal, label = 'Signal v/s Time (Before Removing True Frequencies)', linewidth = 0.5)
plt.plot(time_1, signal_1, label = 'Signal v/s Time (After Removing True Frequencies)', linewidth = 0.8)
plt.title('Plot of Signal v/s Time for the given Signal')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.grid()
plt.legend(loc = 'upper right')

plt.tight_layout(pad = 2.0)

plt.subplot(2, 1, 2)
plt.plot(time, signal, label = 'Signal v/s Time (Before Removing True Frequencies)', linewidth = 0.5)
plt.plot(time_1, signal_1, label = 'Signal v/s Time (After Removing True Frequencies)', linewidth = 0.8)
plt.xlim(0.04, 0.06)
plt.title('Plot of Signal v/s Time $∈$ [0.04, 0.06] for the given Signal')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.grid()
plt.legend(loc = 'upper right')

plt.show()
