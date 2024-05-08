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

case1_beta_frequency = calculate_new_sampling_rate(case1EEG.shape[1], sampling_rate, length)

window_array = create_windows(case1_beta_time_domain, case1_beta_frequency, 5, 0.5)

first_window = window_array[0]

print(f'first window length: {len(first_window)}')

symbolic_sequence = translate_to_symbolic_sequence(first_window)

print(f'first window: {first_window}')
print(f'symbolic sequence: {symbolic_sequence}')
distinct_words = count_words(symbolic_sequence)

print(calculateLZC(35, 130))



##PERMUTATION ENTROPY TESTS ##
"""

case1_beta_PE = PE(case1_beta_time_domain, case1_beta_frequency, window_overlap=0.5)

print(f'case 1 beta PE = {case1_beta_PE} with length {len(case1_beta_PE)}')

case1_beta_PE = np.array(case1_beta_PE[::2]).reshape(-1, 1)
case1BIS_scaled = case1BIS.flatten()[12:]
print(len(case1BIS_scaled))

alpha = 1e-3

model = LinearRegression()
model.fit(case1_beta_PE, case1BIS_scaled)

predicted_values = model.predict(case1_beta_PE)

print("Coefficient:", model.coef_)
print("Intercept:", model.intercept_)
r2 = r2_score(case1BIS_scaled, predicted_values)
print(f'R2 = {r2}')
"""