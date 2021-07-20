import pandas as pd
import numpy as nm
import scipy
import math
from scipy.sparse import linalg as ln
from scipy.linalg import pinv
import cmath


def svd(ratings_array, concepts):
    ratings_array_transpose = ratings_array.transpose()
    
   # for nan to 0 conversion,remove if required 
    nm.nan_to_num(ratings_array, copy=False)
    nm.nan_to_num(ratings_array_transpose, copy=False)
    
    # calculating U matrix
    array_product = nm.dot(ratings_array, ratings_array_transpose)
    #if concepts <= 2:
    #    eigenvalues, eigenvectors_u = nm.linalg.eig(array_product) #--this is will give issues for large matrix
    #else:
    eigenvalues, eigenvectors_u = ln.eigs(array_product, k=concepts) #pass concepts or no of eigenvalues req
    #sorted(eigenvalues, reverse=True)
    # calculating V matrix
    array_product2 = nm.dot(ratings_array_transpose, ratings_array)
    #if concepts <= 2:
    #    eigenvalues_2, eigenvectors_v = nm.linalg.eig(array_product2)
    #else:
    eigenvalues2, eigenvectors_v = ln.eigs(array_product2, k=concepts)
    
    # calculating variance matrix
    #, dtype=nm.complex_)
    eigenvalues_real = nm.zeros(shape=(concepts,))
    eigenvalues_real2 = nm.zeros(shape=(concepts,))
    eigenvectors_u_real = nm.zeros(shape=(concepts,concepts))
    eigenvectors_v_real = nm.zeros(shape=(concepts,concepts))

    for i in range(0, (len(eigenvalues))):
        eigenvalues_real[i] = eigenvalues[i].real
    print('Eig val 1 ', eigenvalues_real)
    for i in range(0, (len(eigenvalues2))):
        eigenvalues_real2[i] = eigenvalues2[i].real
    print('Eig val 2 ', eigenvalues_real2)
    for i in range(0, (len(eigenvalues))):
        for j in range(0, len(eigenvalues)):
            eigenvectors_u_real[i][j] = eigenvectors_u[i][j].real
    print(eigenvectors_u_real)
    for i in range(0, (len(eigenvalues))):
        for j in range(0, len(eigenvalues)):
            eigenvectors_v_real[i][j] = eigenvectors_v[i][j].real
    print(eigenvectors_v_real)

    ind = eigenvalues_real.argsort()[::-1]
    eigenvalues_real = eigenvalues_real[ind]
    eigenvectors_u_real = eigenvectors_u_real[:, ind]

    ind = eigenvalues_real2.argsort()[::-1]
    eigenvalues_real2 = eigenvalues_real2[ind]
    eigenvectors_v_real = eigenvectors_v_real[:, ind]

    print(eigenvalues_real)
    print(eigenvectors_u_real)
    print(eigenvalues_real2)
    print(eigenvectors_v_real)

    zero_index = len(eigenvalues_real)
    for i in range(0, len(eigenvalues_real)):
        if eigenvalues_real[i] < 0:
            zero_index = i
            break

    eigenvectors_u_real = eigenvectors_u_real[:, list(range(0, zero_index))]
    eigenvectors_v_real = eigenvectors_v_real[:, list(range(0, zero_index))]

    sigma = nm.zeros(shape=(zero_index, zero_index))

    for x in range(0, zero_index):
        for y in range(0, zero_index):
            if x == y:
                if(eigenvalues_real[x]>=0):
                    sigma[x][y] = math.sqrt(eigenvalues_real[x])

    return eigenvectors_u_real, eigenvectors_v_real.T, sigma


def get_pseudo_inverse(w_matrix_np):
    pseudo_matrix = pinv(w_matrix_np)
    return pseudo_matrix


def get_pseudo_inverse_2(w_matrix_np):
    pseudo_matrix = nm.linalg.pinv(w_matrix_np)
    return pseudo_matrix

def compute_svd(w_matrix):
    return nm.linalg.svd(w_matrix, full_matrices=True)