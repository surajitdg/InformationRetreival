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
    # if concepts <= 2:
    #    eigenvalues, eigenvectors_u = nm.linalg.eig(array_product) #--this is will give issues for large matrix
    # else:

    eigenvalues, eigenvectors_u = ln.eigs(array_product, k=concepts)  # pass concepts or no of eigenvalues req
    # sorted(eigenvalues, reverse=True)
    # calculating V matrix
    array_product2 = nm.dot(ratings_array_transpose, ratings_array)
    # if concepts <= 2:
    #    eigenvalues_2, eigenvectors_v = nm.linalg.eig(array_product2)
    # else:
    eigenvalues2, eigenvectors_v = ln.eigs(array_product2, k=concepts)

    # calculating variance matrix
    sigma = nm.zeros(shape=(concepts, concepts))  # , dtype=nm.complex_)
    eigenvalues_real = nm.zeros(shape=(concepts,))
    eigenvalues_real2 = nm.zeros(shape=(concepts,))
    eigenvectors_u_real = nm.zeros(shape=(concepts, concepts))
    eigenvectors_v_real = nm.zeros(shape=(concepts, concepts))

    for i in range(0, (len(eigenvalues))):
        eigenvalues_real[i] = eigenvalues[i].real

    for i in range(0, (len(eigenvalues2))):
        eigenvalues_real2[i] = eigenvalues2[i].real

    for i in range(0, (len(eigenvalues))):
        for j in range(0, len(eigenvalues)):
            eigenvectors_u_real[i][j] = eigenvectors_u[i][j].real

    for i in range(0, (len(eigenvalues))):
        for j in range(0, len(eigenvalues)):
            eigenvectors_v_real[i][j] = eigenvectors_v[i][j].real

    index = eigenvalues_real.argsort()[::-1]
    eigenvalues_real = eigenvalues_real[index]
    eigenvectors_u_real = eigenvectors_u_real[:, index]

    print('Eigenvalues real')
    print(eigenvalues_real)
    eigenvalues_real = nm.fliplr([eigenvalues_real])[0]
    eigenvectors_u_real = nm.fliplr(eigenvectors_u_real)

    index2 = eigenvalues_real2.argsort()[::-1]
    eigenvalues_real2 = eigenvalues_real2[index2]
    eigenvectors_v_real = eigenvectors_v_real[:, index2]

    eigenvalues_real2 = nm.fliplr([eigenvalues_real2])[0]
    eigenvectors_v_real = nm.fliplr(eigenvectors_v_real)

    for i in range(0, len(eigenvalues_real)):
        if eigenvalues_real[i] <= 0:
            zero_index = i
            break

    # del_from_vectors = nm.array(list(range(zero_index, len(eigenvalues_real))))

    # mask = nm.in1d(nm.arange(eigenvalues_real.size), del_from_vectors)
    # x = nm.r_(eigenvalues_real[~mask])
    # eigenvalues_real = x

    # mask2 = nm.in1d(nm.arange(eigenvalues_real.size), del_from_vectors)
    eigenvalues_real = eigenvalues_real[list(range(0, zero_index))]
    eigenvectors_u_real = eigenvectors_u_real[:, list(range(0, zero_index))]
    eigenvectors_v_real = eigenvectors_v_real[:, list(range(0, zero_index))]
    # y = nm.r(eigenvectors_u_real[~mask2])

    print('Eigen values real')
    print(eigenvalues_real)
    print('Eigen u real')
    print(eigenvectors_u_real)
    print('Eigen v real')
    print(eigenvectors_v_real)

    for x in range(0, concepts):
        for y in range(0, concepts):
            if x == y:
                # sigma[x][y] = cmath.sqrt((eigenvalues[x]))
                if (eigenvalues_real[x] > 0):
                    sigma[x][y] = math.sqrt(eigenvalues_real[x])

    return eigenvectors_u_real, eigenvectors_v_real, sigma


def get_pseudo_inverse(w_matrix_np):
    pseudo_matrix = pinv(w_matrix_np)
    return pseudo_matrix


def get_pseudo_inverse_2(w_matrix_np):
    pseudo_matrix = nm.linalg.pinv(w_matrix_np)
    return pseudo_matrix


def compute_svd(w_matrix):
    return nm.linalg.svd(w_matrix, full_matrices=True)