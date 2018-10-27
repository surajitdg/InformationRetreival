import csv
import pickle
from movies import Movies, Ratings
from csvreader import save_list_object
from svd import svd, get_pseudo_inverse, get_pseudo_inverse_2, compute_svd
import numpy as np
import random
import math
from utilityfunctions import read_object

base_matrix = ratings_list_base = read_object('objects/test100/base_matrix.pkl')
test_matrix = read_object('objects/test100/test_matrix.pkl')

#base_matrix = np.matrix([[1, 1, 1, 0, 0], [3, 3, 3, 0, 0], [4, 4, 4, 0, 0], [5, 5, 5, 0, 0], [0, 0, 0, 4, 4],
                         #[0, 0, 0, 5, 5], [0, 0, 0, 2, 2]])

#print(base_matrix.item(4, 3))

no_of_users = len(base_matrix)
no_of_movies = 1682

total_sum = 0
col = [0] * no_of_movies
row = [0] * no_of_users

pr_row = [0] * no_of_users
pr_col = [0] * no_of_movies

base_array = np.array([np.array(row) for row in base_matrix])
base_matrix = np.matrix(base_array)


for i in range(no_of_users):
    for j in range(no_of_movies):
        total_sum += base_matrix.item(i, j) * base_matrix.item(i, j)
        row[i] += base_matrix.item(i, j) * base_matrix.item(i, j)
        col[j] += base_matrix.item(i, j) * base_matrix.item(i, j)

for i in range(no_of_users):
    pr_row[i] = row[i]*1.0/total_sum

for i in range(no_of_movies):
    pr_col[i] = col[i]*1.0/total_sum

print(pr_row)
print(pr_col)

r = 256
#ran_col = [1,3]
#ran_row = [5,3]

ran_row = random.sample(range(0, no_of_users-1), r)
ran_col = random.sample(range(0, no_of_movies-1), r)

#ran_row.sort()
#ran_col.sort()

#print(ran_col)
#print(ran_row)


#c_matrix = [[0 for x in range(r)] for y in range(no_of_users)]
#r_matrix = [[0 for x in range(no_of_movies)] for y in range(r)]
w_matrix = []
c_matrix = []
r_matrix = []

#print(c_matrix)
#print(r_matrix)

for i in range(no_of_users):
    c_matrix.append([])
    for j in range(r):
        x = math.sqrt(r*pr_col[ran_col[j]])*1.0
        if x == 0:
            data = 0
        else:
            data = (base_matrix.item(i, ran_col[j])) / x
        c_matrix[i].insert(j, data)

for i in range(r):
    r_matrix.append([])
    for j in range(no_of_movies):
        x = math.sqrt(r * pr_row[ran_row[i]])
        if x == 0:
            data = 0
        else:
            data = (base_matrix.item(ran_row[i], j)) / x
        r_matrix[i].insert(j, data)


for i in range(r):
    w_matrix.append([])
    for j in range(r):
        w_matrix[i].insert(j, base_matrix.item(ran_row[i], ran_col[j]))

c_matrix_np = np.matrix(c_matrix)
r_matrix_np = np.matrix(r_matrix)
w_matrix_np = np.matrix(w_matrix)

print('************************  C - Matrix  ***********************************')
print(c_matrix_np)
print('************************  R - Matrix  ***********************************')
print(r_matrix_np)
print('************************  W - Matrix  ***********************************')
print(w_matrix_np)

svd_object = svd(w_matrix_np, r)#int(r/2))

u_matrix = svd_object[0]
v_matrix = svd_object[1]
sigma_matrix = svd_object[2]


pseudo_matrix_1 = get_pseudo_inverse(sigma_matrix)
pseudo_matrix_2 = get_pseudo_inverse_2(sigma_matrix)



print('***********************************************************')

print('************************  U - Matrix  ***********************************')
print(np.matrix(u_matrix))
print('************************  V - Matrix  ***********************************')
print(np.matrix(v_matrix))
print('************************  E - Matrix  ***********************************')
print(np.matrix(sigma_matrix))


print('************************  Pseudo - Matrix - scipy  ***********************************')
print(np.matrix(pseudo_matrix_1))
print('************************  Pseudo - Matrix - numpy  ***********************************')
print(np.matrix(pseudo_matrix_2))

pseudo_square_matrix = np.matrix(pseudo_matrix_1)*np.matrix(pseudo_matrix_1)
print('************************  Pseudo - Matrix - square  ***********************************')

print(pseudo_square_matrix)

x_transpose = np.matrix(u_matrix).transpose()
y = np.matrix(v_matrix)

print('************************  X Transpose ***********************************')
print(x_transpose)

print('************************  Y Transpose ***********************************')
print(y)
print(y.shape, pseudo_square_matrix.shape, x_transpose.shape)
u_matrix = y*pseudo_square_matrix*x_transpose

print('************************  U Matrix  ***********************************')
print(u_matrix)

temp = u_matrix * r_matrix_np
final_cur = c_matrix_np * temp

print('************************  Final CUR Matrix  ***********************************')

print(final_cur)

print('************************  A - CUR Matrix ***********************************')

diff_matrix = base_matrix - final_cur
print(diff_matrix)


'''
svd_u, svd_v, svd_sigma = svd(base_matrix, 3)

print(svd_u)
print(svd_sigma)
print(np.matrix(svd_v).transpose())

#final_svd = np.matrix(svd_u) * np.matrix(svd_sigma) * np.matrix(svd_v).transpose()

print('************************  Final SVD Matrix  ***********************************')

#print(final_svd)

print('************************  SVD - A Matrix ***********************************')

#diff_matrix_2 = final_svd - base_matrix
#print(diff_matrix_2)'''

