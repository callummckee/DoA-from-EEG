import numpy as np

def calculate_new_sampling_rate(original_signal_length, original_signal_sampling_rate, new_signal_length):
    original_signal_duration = original_signal_length/original_signal_sampling_rate
    frequency = new_signal_length/original_signal_duration
    return frequency

def create_windows(data, sampling_rate, window_length, overlap):
    """
    data is an array of EEG signals with a frequency of sampling_rate
    returns an array whose elements are arrays with data of duration window_length (in seconds)
    overlap is a fraction representing the portion of each window that is present in the previous window
    """
    window_array = []
    data_length = len(data)
    window_length_samples = int(sampling_rate * window_length)
    step_size = int((1 - overlap) * window_length_samples)
    for i in range(0, data_length - window_length_samples + 1, step_size):
        window_array.append(data[i:i + window_length_samples])
    return window_array

def convert_decomposed_to_time_domain(decomposed_frequency_data):
    decomposed_time_domain = []
    number_of_cases = len(decomposed_frequency_data)
    for i in range(number_of_cases):
        case_time_domain = {}
        for frequency_band, band_data in decomposed_frequency_data[i].items():
            frequency_band_time_domain = np.fft.ifft(band_data).real #converts the data in the frequency band to the time domain and takes the real part
            case_time_domain[frequency_band] = frequency_band_time_domain
        decomposed_time_domain.append(case_time_domain)
    return decomposed_time_domain

def operation_on_multiple_case_data(decomposed_time_domain_data, operation, original_signal_sample_rate, original_signal_lengths):
    output = []
    number_of_cases = len(decomposed_time_domain_data)
    for i in range(number_of_cases):
        case_output = {}
        for frequency_band, band_data in decomposed_time_domain_data[i].items():
            new_sample_rate = calculate_new_sampling_rate(original_signal_lengths[i], original_signal_sample_rate, len(band_data))
            frequency_band_output = operation(band_data, new_sample_rate)
            case_output[frequency_band] = frequency_band_output
        output.append(case_output)
    return output
    
def convert_decomposed_amplitude_to_power(decomposed_time_domain_data):
    output = []
    number_of_cases = len(decomposed_time_domain_data)
    for i in range(number_of_cases):
        case_output = {}
        for frequency_band, band_data in decomposed_time_domain_data[i].items():
             frequency_band_output = []
             for amplitude in band_data:
                 power = amplitude ** 2
                 frequency_band_output.append(power)
             case_output[frequency_band] = frequency_band_output
        output.append(case_output)
    return output