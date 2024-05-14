import numpy as np
import math
from utils import *


def calculate_mobility(band_data, sampling_rate, window_seconds, window_overlap):
    """
    'band_data' is an list of signal values for a specific frequency band in the time domain
    'sampling_rate' is the frequency of 'band_data' in Hz
    'window_seconds' is the duration of each window that the mobility is calculated for
    'window_overlap' is a fraction representing the portion of each previous window that is present in the subsequent window

    returns an array of mobility values for each of the windows segmented from 'band_data'
    """
    mobility_array = []

    window_array = create_windows(band_data, sampling_rate, window_seconds, window_overlap)
    for window in window_array:
        window_derivative = np.gradient(window)
        variance = np.var(window)
        variance_derivative = np.var(window_derivative)
        mobility = math.sqrt(variance_derivative/variance)
        mobility_array.append(mobility)
    
    return mobility_array


