import numpy as np
from skimage.restoration import denoise_nl_means, estimate_sigma
import matplotlib.pyplot as plt


def non_local_means(data):
    """
    data is a 2d numpy array of EEG signals, returns the same array denoised
    """
    sigma = estimate_sigma(data) #calculates the standard deviation of Gaussian noise in the data 
    denoised_data = denoise_nl_means(
        data, 
        h = sigma #controls the degree of filtering applied to the signal, considered a rule of thumb to use sigma
    )
    return np.reshape(denoised_data, (1, len(denoised_data)))

def plot_noised_vs_denoised(noised, denoised):
    noised_sample = noised[0]
    denoised_sample = denoised[0]
    plt.figure(figsize=(10, 5))

    plt.plot(noised_sample, label = "Original Data", alpha = 1)
    plt.plot(denoised_sample, label = "Denoised Data", alpha = 0.5)

    plt.legend()
    plt.xlabel('Index')
    plt.ylabel('Voltage')
    plt.grid(True)
    plt.show()