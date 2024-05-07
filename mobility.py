import numpy as np
import math
import matplotlib.pyplot as plt
from utils import *

window_seconds = 56 
overlap_seconds = 55 #s
sampling_rate = 128 #Hz


def calculate_mobility(band_data, window_seconds, overlap_seconds, original_signal_length):
    """
    band_data is a 1d array of voltage
    mobility_array has length equal to len(band_data) // sampling_rate (actually it doesn't but should in this specific case, leaving this here to fix later)
    each value of mobility_array should represent the mobility of the signal at time (window_seconds - overlap_seconds)
    
    It is assumed (because I don't know how else to do this) that the frequency components of the signal are spread evenly across the signal.
    Therefore, the time interval represented by the index of the ifft calculated from a specific band (beta etc.) 
    can be calculated by original_signal_length/len(band_data)
    """
    mobility_array = []




    time_domain = np.fft.ifft(band_data).real #converts band_data, which is in the frequency domain to the time domain
    length = len(time_domain)
    interval = original_signal_length/length
    print(f'accurate_frequency: {1/interval}')
    frequency = int(1//interval)
    print(f'frequency: {frequency}')
    print(f'interval: {interval}')

    window_size = window_seconds * frequency
    overlap_size = overlap_seconds * frequency

    print(f'length of time_domain = {length}')
    derivative = np.gradient(time_domain) #computes the derivative with respect to time of the time domain data
    print(f'length of derivative: {len(derivative)}')

    for i in range(0, length - window_size, window_size - overlap_size):
        window = time_domain[i: window_size + i]
        window_derivative = derivative[i: window_size + i]
        variance = np.var(window)
        variance_derivative = np.var(window_derivative)
        mobility = math.sqrt(variance_derivative/variance)
        mobility_array.append(mobility)
    
    return mobility_array, interval

def plot_mobility_vs_bis(mobility, bis):
    """
    expects the data to already be scaled
    """
    plt.figure(figsize=(20, 10))

    plt.plot(mobility, bis)
    plt.title("BIS vs Mobility for Beta Frequency") #Make more general
    plt.xlabel('Mobility')
    plt.ylabel('BIS')
    plt.grid(True)
    plt.show()


