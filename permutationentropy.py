import numpy as np
from itertools import permutations
from math import log
from utils import create_windows

time_delay = 5 #s
pe_vector_overlap = 0.5 #as a fraction

def create_m_dimension_vectors(data, m, sampling_rate, overlap, L = 1):
    """
    m is the embedding dimension
    overlap is a fraction representing the proportion of each previous vector that is present in the subsequent vector

    returns X, a set of m-dimension vectors
    """
    X = []
    signal_dim = len(data)
    step_size = int(m * L * (1 - overlap))

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


def entropy_calculation(possible_orders, index_vectors):
    PE = 0
    for order in possible_orders:
        count = index_vectors.count(order)
        if count > 0:
            p_i =   count/len(index_vectors)
            PE += p_i*(log(p_i))
    
    return -PE


def PE(data, sampling_rate, pe_vector_overlap = 0.5, window_overlap = 0.5, window_length = 5, m = 4):
    window_array = create_windows(data, sampling_rate, window_length, window_overlap)
    orders = possible_orders(m)

    pe_array = []

    for window in window_array:
        m_dimension_vectors = create_m_dimension_vectors(window, m, sampling_rate, pe_vector_overlap)
        index_vectors = PE_sort(m_dimension_vectors)
        pe = entropy_calculation(orders, index_vectors)
        pe_array.append(pe)
    return pe_array


