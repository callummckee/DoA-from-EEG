import numpy as np
import matplotlib.pyplot as plt


bands = {
    'Delta' : (0.5, 3.5),
    'Theta' : (3.5, 7),
    'Alpha' : (7, 13),
    'Beta' : (13, 38.5), 
    'Gamma' : (38.5, 64),
    'Beta b': (21.5, 30),
    'Gamma 1': (30, 38.5),
    'Gamma 2': (38.6, 47),
    'Gamma 3': (47, 55.5), 
    'Gamma 4': (55.5, 64),
    'Gamma a': (30, 47), 
    'Gamma b': (47, 64),
    'Beta a': (13, 21.5),
    'Alpha a': (7, 10),
    'Alpha b': (10, 13), 
    'Beta 1': (13, 17),
    'Beta 2': (17, 21.5), 
    'Beta 3': (21.5, 26), 
    'Beta 4': (26, 30), 
    'Beta gamma': (21.5, 38.5)
}

def fft(data, sampling_rate):
    """
    Decomposes time domain signal into the frequency bands outlined in 'bands'.
    'data' is a one dimensional list of signal values.
    'sampling_rate' specifies the frequency of the data in Hz.
    Returns a dictionary object where the keys are the same as 'bands' and the values are
    complex numbers representing amplitude and phase information across the range of values specified in 'bands'.
    """
    fft_result = np.fft.fft(data)
    frequencies = np.fft.fftfreq(len(data), 1/sampling_rate)
    band_array = {}
    for band_name, (low, high) in bands.items():
        band_filter = (frequencies >=low) & (frequencies <= high)
        band_array[band_name] = fft_result[band_filter]
    return band_array


def plot_frequency_bands(band_array, frequencies):
    plt.figure(figsize=(20, 10))
    num_bands = len(band_array)

    for i, (band_name, band_data) in enumerate(band_array.items(), 1):
        plt.subplot(1, num_bands, i)


        band_frequencies = frequencies[(frequencies >= bands[band_name][0]) & (frequencies <= bands[band_name][1])]
        band_magnitude = np.abs(band_data)

        plt.plot(band_frequencies, band_magnitude)
        plt.title(band_name)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.grid(True)
    plt.tight_layout
    plt.show()



