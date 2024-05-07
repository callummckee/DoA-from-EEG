def calculate_new_sampling_rate(original_signal_length, original_signal_sampling_rate, new_signal_length):
    original_signal_duration = original_signal_length/original_signal_sampling_rate
    frequency = new_signal_length/original_signal_duration
    print(f'frequency: {frequency}')

    return frequency

    
