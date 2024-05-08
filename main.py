from importdata import data
from fft import *
from mobility import *
from logistic_regression import *
from permutationentropy import *
from utils import *
from lempelziv import *
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

sampling_rate = 128 #Hz

train_data = data[::2] #select every second case for training
    
eeg_train_data = [case['EEG'] for case in train_data]
bis_train_data = [case['bis'] for case in train_data]

decomposed_eeg_train_data = [fft(case) for case in eeg_train_data]
decomposed_eeg_train_time_domain = convert_decomposed_to_time_domain(decomposed_eeg_train_data)
decomposed_eeg_train_time_domain_power = convert_decomposed_amplitude_to_power(decomposed_eeg_train_time_domain)

signal_lengths = [len(case[0]) for case in eeg_train_data] 

mobility_amplitude_array = operation_on_multiple_case_data(decomposed_eeg_train_time_domain, calculate_mobility, sampling_rate, signal_lengths)
print(f'mobility amplitude array length: {len(mobility_amplitude_array)}')
pe_amplitude_array = operation_on_multiple_case_data(decomposed_eeg_train_time_domain, PE, sampling_rate, signal_lengths)
print(f'pe array amplitude length: {len(pe_amplitude_array)}')
lzc_amplitude_array = operation_on_multiple_case_data(decomposed_eeg_train_time_domain, LZC_single_band, sampling_rate, signal_lengths)
print(f'lzc array amplitude length: {len(lzc_amplitude_array)}')

mobility_power_array = operation_on_multiple_case_data(decomposed_eeg_train_time_domain_power, calculate_mobility, sampling_rate, signal_lengths)
print(f'mobility array length: {len(mobility_amplitude_array)}')
pe_power_array = operation_on_multiple_case_data(decomposed_eeg_train_time_domain_power, PE, sampling_rate, signal_lengths)
print(f'pe array length: {len(pe_amplitude_array)}')
lzc_power_array = operation_on_multiple_case_data(decomposed_eeg_train_time_domain_power, LZC_single_band, sampling_rate, signal_lengths)
print(f'lzc array length: {len(lzc_amplitude_array)}')

















"""

model = LinearRegression()
model.fit(case1_beta_PE, case1BIS_scaled)

predicted_values = model.predict(case1_beta_PE)

print("Coefficient:", model.coef_)
print("Intercept:", model.intercept_)
r2 = r2_score(case1BIS_scaled, predicted_values)
print(f'R2 = {r2}')
"""