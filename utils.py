import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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
    """
    Applies the inverse fourier transform on an array where each element in the array is
    a dictionary representing EEG data in the frequency domain decomposed into frequency bands.
    Returns an array where each element is a dictionary representing EEG data in the time domain
    decomposed into the same frequency bands. 
    """
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
    """
    Extracts features from an 'decomposed_time_domain_data' using the function 'operation'.
    """
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
    """
    Takes an array where each element is a dictionary 
    """
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

def associate_features_with_BIS(feature_array, bis_data, window_length, window_overlap, bis_sample_rate):
    """
    Combines the features for frequency bands across cases, scales both these features and the associated BIS data such
    that they are of the same length. Returns a dictionary where the keys are frequency bands and the values are an array with 
    two nested arrays of the same length reprenting the feature values and the associated BIS values.
    """
    frequency_band_output = {}
    number_of_cases = len(feature_array)
    duration = window_length * window_overlap #seconds per data point in feature_array
    bis_duration = 1/bis_sample_rate #seconds per data point in bis_data
    scaling_factor = int(round(bis_duration/duration))
    print(f'scaling_factor: {scaling_factor}')
    for frequency_band in feature_array[0].keys():
        frequency_band_values = []
        bis_values = []
        print(f'frequency_band: {frequency_band}')
        for i in range(number_of_cases):
            print(f'length of unscaled feature data: {len(feature_array[i][frequency_band])}')
            if scaling_factor > 0:
                feature_data = feature_array[i][frequency_band][::scaling_factor]
            else:
                feature_data = feature_array[i][frequency_band]
            feature_data_length = len(feature_data)
            flattened_bis = bis_data[i].flatten() #probably move outside of function
            print(f'length of untrimmed bis: {len(flattened_bis)}')
            flattened_bis_length = len(flattened_bis)
            if flattened_bis_length > feature_data_length:
                scaled_bis_data = flattened_bis[flattened_bis_length - feature_data_length:].tolist()
            elif feature_data_length > flattened_bis_length:
                feature_data = feature_data[feature_data_length - flattened_bis_length:]
                scaled_bis_data = flattened_bis.tolist()
            frequency_band_values += feature_data
            bis_values += scaled_bis_data
        frequency_band_output[frequency_band] = [frequency_band_values, bis_values]
    
    return frequency_band_output

def test_associate_features_with_bis(feature_bis_dict):
    for frequency_band in feature_bis_dict.keys():
        print(frequency_band)
        print(f'values_length: {len(feature_bis_dict[frequency_band][0])}')
        print(f'bis_length: {len(feature_bis_dict[frequency_band][1])}')
    return

def linear_regression(feature_bis_dict):
    correlation_by_band = {}
    for frequency_band, data in feature_bis_dict.items():
        model = LinearRegression()
        data[0] = np.array(data[0]).reshape(-1, 1)
        data[1] = np.array(data[1])
        model.fit(data[0], data[1])

        predicted_values = model.predict(data[0])

        print(frequency_band)
        print("Coefficient:", model.coef_)
        print("Intercept:", model.intercept_)

        r2 = r2_score(data[1], predicted_values)
        correlation_by_band[frequency_band] = r2
    
    return correlation_by_band
