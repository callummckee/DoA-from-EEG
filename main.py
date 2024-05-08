import numpy as np

from NLM import *
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

#print(f'data: {type(data)}')
#print(f'data[0] type: {type(data[0])}')

train_data = data[::2] #select every second case for training
    
eeg_train_data = [case['EEG'] for case in train_data]
bis_train_data = [case['bis'] for case in train_data]
#print(f'eeg_train_data: {eeg_train_data}')
#print(f'bis train data: {bis_train_data}')

decomposed_eeg_train_data = [fft(case) for case in eeg_train_data]

#print(f'decomposed_eeg_train_data: {decomposed_eeg_train_data}')


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

decomposed_eeg_train_time_domain = convert_decomposed_to_time_domain(decomposed_eeg_train_data)
print(f'decomposed_eeg_train_time_domain: {decomposed_eeg_train_time_domain}')



signal_lengths = [len(case[0]) for case in eeg_train_data] 


def operation_on_multiple_case_data(decomposed_time_domain_data, operation, original_signal_sample_rate):
    output = []
    number_of_cases = len(decomposed_time_domain_data)
    for i in range(number_of_cases):
        case_output = {}
        for frequency_band, band_data in decomposed_time_domain_data[i].items():
            new_sample_rate = calculate_new_sampling_rate(signal_lengths[i], original_signal_sample_rate, len(band_data))
            frequency_band_output = operation(band_data, new_sample_rate)
            case_output[frequency_band] = frequency_band_output
        output.append(case_output)
    return output

mobility_array = operation_on_multiple_case_data(decomposed_eeg_train_time_domain, calculate_mobility, original_signal_sample_rate=128)
print(f'mobility array length: {len(mobility_array)}')


pe_array = operation_on_multiple_case_data(decomposed_eeg_train_time_domain, PE, original_signal_sample_rate=128)
print(f'pe array length: {len(pe_array)}')


lzc_array = operation_on_multiple_case_data(decomposed_eeg_train_time_domain, LZC_single_band, original_signal_sample_rate=128)
print(f'lzc array length: {len(lzc_array)}')














##PERMUTATION ENTROPY TESTS ##
"""

model = LinearRegression()
model.fit(case1_beta_PE, case1BIS_scaled)

predicted_values = model.predict(case1_beta_PE)

print("Coefficient:", model.coef_)
print("Intercept:", model.intercept_)
r2 = r2_score(case1BIS_scaled, predicted_values)
print(f'R2 = {r2}')
"""