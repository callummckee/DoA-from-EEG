def calculate_new_sampling_rate(original_signal_length, original_signal_sampling_rate, new_signal_length):
    original_signal_duration = original_signal_length/original_signal_sampling_rate
    frequency = new_signal_length/original_signal_duration
    print(f'frequency: {frequency}')

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
    window_array = [window.tolist() for window in window_array]
    return window_array
    
def convert_amplitude_to_power(data):
    power_array = []
    for amplitude in data:
        power = amplitude ** 2
        power_array.append(power)