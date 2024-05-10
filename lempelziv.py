import numpy as np
from math import log2
from utils import create_windows

def translate_to_symbolic_sequence(data):
    """
    Calculates a 1/0 symbolic sequence by comparing the each point of the signal to
    the median value of the signal (threshold value). If the point is greater than
    the threshold value, a 1 is added to the sequence, if it is less a 0 is added to the sequence.
    """
    threshold = np.median(data)
    symbolic_sequence = []
    for value in data:
        if value >= threshold:
            symbolic_sequence.append(1)
        else:
            symbolic_sequence.append(0)
    return symbolic_sequence

def count_words(symbolic_sequence):
    """
    Produces a sequence of "words" (binary sequences), W, from the symbolic sequence with
    the following method. 
    The first word is the the first element of the symbolic sequence. Each subsequent word
    is the shortest that can be constructed from consecutive elements of the symbolic sequence
    that has not yet appeared in W. 
    
    Returns the number of distinct words in W.
    """
    words = []
    length = len(symbolic_sequence)
    i = 0
    while i < length:
        word = [symbolic_sequence[i]]
        while word in words:
            i += 1
            if i == length:
                return len(words)
            word.append(symbolic_sequence[i])
        words.append(word)
        i += 1
    return len(words)

def calculateLZC(distinct_words, signal_length):
    lzc = (distinct_words*(log2(distinct_words) + 1))/signal_length
    return lzc

def LZC_single_band(data, sampling_rate, window_length, window_overlap):
    window_array = create_windows(data, sampling_rate, window_length, window_overlap)

    lzc_array = []

    for window in window_array:
        signal_length = len(window)
        symbolic_sequence = translate_to_symbolic_sequence(window)
        distinct_words = count_words(symbolic_sequence)
        lzc = calculateLZC(distinct_words, signal_length)
        lzc_array.append(lzc)
    return lzc_array



    


    