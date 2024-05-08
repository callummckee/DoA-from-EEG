import numpy as np
import matplotlib.pyplot as plt

bands = {
    'Delta' : (0.5, 3.5),
    'Theta' : (3.5, 7),
    'Alpha' : (7, 13),
    'Beta' : (13, 38.5), 
    'Gamma' : (38.5, 64)
}

def fft(data, sampling_rate = 128):
    data = data[0] #fix later if dimension of array is > 1 reshape to 1
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



