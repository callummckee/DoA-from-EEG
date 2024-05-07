from NLM import *
from importdata import data
from fft import *
from mobility import *
from logistic_regression import *
from permutationentropy import *
from utils import *
from sklearn.metrics import r2_score

sampling_rate = 128 #Hz

    


print (data[0])

case1EEG = data[0]['EEG']
case1BIS = data[0]['bis']


original_signal_length = (case1EEG.shape[1])/sampling_rate #in seconds
print(f'original_signal_length {original_signal_length}')


print(f'case1EEG shape: {case1EEG.shape}')
print(f'case1bis shape: {case1BIS.shape}')
#print("case1EEGsample", case1EEGsample)
#print(f"min: {np.min(case1EEGsample)} max: {np.max(case1EEGsample)}")
#print(case1EEGsample.shape)
band_array = fft(case1EEG)
print(f'band_array type: {type(band_array)}')
#print("band array", band_array)
print(f'beta shape: {band_array["Beta"].shape}')
#denoised_case1EEGsample = non_local_means(case1EEGsample)
#print(denoised_case1EEGsample.shape)
case1_beta_mobility, case1_beta_interval = calculate_mobility(band_array["Beta"], window_seconds, overlap_seconds, original_signal_length) #fix up how parameters are passed

#print(f'Case1_beta_mobility length = {len(case1_beta_mobility)}')
#case1_beta_mobility_scaled = np.array(case1_beta_mobility[::5])
#print(len(case1_beta_mobility_scaled))
#case1BIS_scaled = case1BIS.flatten()[0:745]
#print(len(case1BIS_scaled))

#alpha = 1

#w, b = gradientDescent(case1_beta_mobility_scaled, case1BIS_scaled, alpha)


#predicted_values = predict(case1_beta_mobility_scaled, w, b)

#r2 = r2_score(case1BIS_scaled, predicted_values)
#print(f'R2 = {r2}')
#plot_noised_vs_denoised(case1EEGsample, denoised_case1EEGsample)

case1_beta_time_domain = np.fft.ifft(band_array["Beta"]).real
length = len(case1_beta_time_domain)

print(f'case1EEG.shape[1]: {case1EEG.shape[1]}')
print(f'case1_beta time domain length: {length}')


case1_beta_frequency = calculate_new_sampling_rate(case1EEG.shape[1], sampling_rate, length)


PE_vectors = create_m_dimension_vectors(case1_beta_time_domain, m, case1_beta_frequency, time_delay, overlap)
print(PE_vectors[:5])

PE_vectors_sorted = PE_sort(PE_vectors)
print(PE_vectors_sorted[:5])

possible_orders = possible_orders(4)

PE = permutation_entropy(possible_orders, PE_vectors_sorted)

print(f'PE: {PE}')

