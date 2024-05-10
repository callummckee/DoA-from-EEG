# Assessing Depth of Anaesthesia using EEG data
Attempting to implement the ideas from the paper "Depth of anaesthesia assessment based on adult
electroencephalograph beta frequency band" by Dr. Tianning Li and Dr. Peng Wen (found here: https://link.springer.com/article/10.1007/s13246-016-0459-5) using a publicly available dataset (found here: https://figshare.com/articles/dataset/EEG_and_BIS_raw_data/5589841). 

This is my first attempt at anything related to signal processing or time-series data. I have tried to limit my use of libraries where possible in order to cement my understanding of the employed concepts. 

Graphs displaying the coefficient of determination for each extracted feature for each frequency band can be found in the Graphs folder. The x-axis of the graphs represents the frequency bands defined in fft.py with indices 1-20 representing the amplitude of these frequency bands and indices 21-40 representing the power.


