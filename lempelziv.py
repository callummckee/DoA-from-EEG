import numpy as np
from math import log2

def translate_to_symbolic_sequence(data):
    """
    Calculates a 1/0 symbolic sequence by comparing the each point of the signal to
    the median value of the signal (threshold value). If the point is greater than
    the threshold value, a 1 is added to the sequence, if it is less a 0 is added to the sequence.
    """
    threshold = np.median(data)
    print(f'threshold: {threshold}')
    symbolic_sequence = []
    for value in data:
        if value >= threshold:
            symbolic_sequence.append(1)
        else:
            symbolic_sequence.append(0)
    return symbolic_sequence

def count_words(symbolic_sequence):
    words = []
    length = len(symbolic_sequence)
    i = 0
    while i < length:
        word = [symbolic_sequence[i]]
        while word in words:
            i += 1
            if i == length:
                print(f'words: {words}')
                print(f'distinct words: {len(words)}')
                return len(words)
            word.append(symbolic_sequence[i])
        words.append(word)
        i += 1
    print(f'words: {words}')
    print(f'distinct words: {len(words)}')
    return len(words)

def calculateLZC(distinct_words, signal_length):
    lzc = (distinct_words*(log2(distinct_words) + 1))/signal_length
    return lzc



    


    