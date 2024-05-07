import numpy as np
from itertools import permutations
from math import log

time_delay = 5 #s
overlap = 0.5 #as a fraction
m = 4

def create_m_dimension_vectors(data, m, sampling_rate, time_delay, overlap):
    """
    m is the embedding dimension
    overlap is a fraction representing the proportion of each previous vector that is present in the subsequent vector

    returns X, a set of m-dimension vectors
    """
    X = []
    print(f'sampling_rate = {sampling_rate}')
    print(f'time_delay = {time_delay}')
    L = sampling_rate * time_delay
    print(f'L: {L}')
    signal_dim = data.shape[0]
    print(f'signal_dim = {signal_dim}')
    step_size = int(m * L * (1 - overlap))
    print(f'step_size: {step_size}')

    for i in range(0, signal_dim - (m*L) + 1, step_size):
        x = []
        for j in range(i, i + m*L, L):
            x.append(data[j])
        X.append(x)
            

    return X

def PE_sort(m_dimension_vectors):
    X = []
    for vector in m_dimension_vectors:
        sorted_vector = sorted(vector)
        index_form = []
        for element in vector:
            index = sorted_vector.index(element) + 1
            index_form.append(index)
        X.append(index_form)
    
    return X



def possible_orders(m):
    """
    returns an array, M, of length m! whose elements are all possible orders of m elements.
    """
    values = list(range(1, m+1))
    permutation_output = list(permutations(values))
    M = [list(order) for order in permutation_output]

    return M


def permutation_entropy(possible_orders, index_vectors):
    PE = 0
    for order in possible_orders:
        count = index_vectors.count(order)
        p_i =   count/len(index_vectors)
        PE += p_i*(log(p_i))
    
    return -PE
