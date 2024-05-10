import numpy as np
import math
import matplotlib.pyplot as plt
from utils import *


def calculate_mobility(band_data, sampling_rate, window_seconds, window_overlap):
    mobility_array = []

    window_array = create_windows(band_data, sampling_rate, window_seconds, window_overlap)

    for window in window_array:
        window_derivative = np.gradient(window)
        variance = np.var(window)
        variance_derivative = np.var(window_derivative)
        mobility = math.sqrt(variance_derivative/variance)
        mobility_array.append(mobility)
    
    return mobility_array

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


