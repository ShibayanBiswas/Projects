import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
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

yf = np.abs(fft(signal))/1000
# xf = fftfreq(Number of Samples, ((time[999] - time[0])/(Number of Samples)))
xf = fftfreq(1000, 0.0001)

rfreq = list()

for i in range(0, 999):
    if yf[i] > 0.15 and xf[i] > 0 :
        rfreq.append(xf[i])

print("The resultant Frequencies : ")
for i in rfreq:
    print("\t", i)
    
