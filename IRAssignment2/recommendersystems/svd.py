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
    if concepts <= 2:
        eigenvalues, eigenvectors_u = nm.linalg.eig(array_product) #--this is will give issues for large matrix
    else:
        eigenvalues, eigenvectors_u = ln.eigs(array_product, k=concepts) #pass concepts or no of eigenvalues req
    sorted(eigenvalues, reverse=True)
    # calculating V matrix
    array_product2 = nm.dot(ratings_array_transpose, ratings_array)
    if concepts <= 2:
        eigenvalues_2, eigenvectors_v = nm.linalg.eig(array_product2)
    else:
        eigenvalues2, eigenvectors_v = ln.eigs(array_product2, k=concepts)
    
    # calculating variance matrix
    sigma = nm.zeros(shape=(concepts, concepts), dtype=nm.complex_)
    eigenvalues_real = nm.zeros(shape=(concepts,))

    #for i in range(0, (len(eigenvalues)-1)):
        #eigenvalues_real[i] = eigenvalues[i].real
        
    for x in range(0, concepts):
        for y in range(0, concepts):
            if x == y:
                sigma[x][y] = cmath.sqrt((eigenvalues[x]))
                #sigma[x][y] = math.sqrt(eigenvalues[x])

    return eigenvectors_u, eigenvectors_v, sigma


def get_pseudo_inverse(w_matrix_np):
    pseudo_matrix = pinv(w_matrix_np)
    return pseudo_matrix


def get_pseudo_inverse_2(w_matrix_np):
    pseudo_matrix = nm.linalg.pinv(w_matrix_np)
    return pseudo_matrix

def compute_svd(w_matrix):
    return nm.linalg.svd(w_matrix, full_matrices=True)