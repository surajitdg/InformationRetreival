import csv
import pickle
from movies import Movies, Ratings
from csvreader import save_list_object
from svd_recommender import svd
import numpy as np
import random
import math
import cmath
from utilityfunctions import read_object
import time


#from svd_recommender import svd
start_time = time.time()
#base_matrix = read_object('objects/test100/base_matrix.pkl')
test_matrix = read_object('objects/test100/test_matrix.pkl')

base_matrix = np.array([[1, 1, 1, 0, 0], [3, 3, 3, 0, 0], [4, 4, 4, 0, 0], [5, 5, 5, 0, 0], [0, 0, 0, 4, 4],
                        [0, 0, 0, 5, 5], [0, 0, 0, 2, 2]])

#print(base_matrix.item(4, 3))

#base_array = np.array([np.array(row) for row in base_matrix])
test_array = np.array([np.array(row) for row in test_matrix])

final_matrix = base_matrix #+ test_matrix


#print('Base matrix dimensions', base_matrix.shape[0], base_matrix.shape[1])

no_of_users = len(base_matrix)
no_of_movies = len(base_matrix[0])

total_sum = 0
col = [0] * no_of_movies
row = [0] * no_of_users

pr_row = [0] * no_of_users
pr_col = [0] * no_of_movies

for i in range(no_of_users):
    for j in range(no_of_movies):
        total_sum += base_matrix.item(i, j) * base_matrix.item(i, j)
        row[i] += base_matrix.item(i, j) * base_matrix.item(i, j)
        col[j] += base_matrix.item(i, j) * base_matrix.item(i, j)

for i in range(no_of_users):
    pr_row[i] = row[i]*1.0/total_sum

for i in range(no_of_movies):
    pr_col[i] = col[i]*1.0/total_sum

#print(pr_row)
#print(pr_col)

r = np.linalg.matrix_rank(base_matrix)

'''for i in range(0, r):
    ran_row.append(np.random.choice(list(range(0, no_of_users)), pr_row))
    ran_col.append(np.random.choice(list(range(no_of_movies)), pr_col))
'''
#print(ran_row)
#print(ran_col)

row_ids = list(range(0, no_of_users))
col_ids = list(range(0, no_of_movies))

ran_row = []
ran_col = []

for i in range(0, r, 1):
    ran_row.append(random.choices(row_ids, pr_row)[0])
    ran_col.append(random.choices(col_ids, pr_col)[0])


px_row = []
px_col = []

for i in ran_row:
    px_row.append(pr_row[i])

for i in ran_col:
    px_col.append(pr_col[i])


px_row = np.array(px_row)
ran_row = np.array(ran_row)
ind = px_row.argsort()[::-1]
px_row = px_row[ind]
ran_row = ran_row[ind]

px_col = np.array(px_col)
ran_col = np.array(ran_col)
ind = px_col.argsort()[::-1]
px_col = px_col[ind]
ran_col = ran_col[ind]

ran_col = [1,4]
ran_row = [4,1]


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

#svd_object = np.linalg.svd(w_matrix_np)

u_matrix = svd_object[0]
v_matrix = svd_object[1]
sigma_matrix = svd_object[2]

print('Sigma dimensions ', np.matrix(sigma_matrix).shape)
print('U dimensions ', np.matrix(u_matrix).shape)
print('V dimensions ', np.matrix(v_matrix).shape)

print('***********************************************************')

print('************************  U - Matrix  ***********************************')
print(np.matrix(u_matrix))
print('************************  V - Matrix  ***********************************')
print(np.matrix(v_matrix))
print('************************  E - Matrix  ***********************************')
print(np.matrix(sigma_matrix))


x_transpose = np.matrix(u_matrix).transpose()
y_transpose = np.matrix(v_matrix).transpose()

sig_rows = np.matrix(sigma_matrix).shape[0]
sig_cols = np.matrix(sigma_matrix).shape[1]

z = np.zeros(shape=(sig_rows, sig_cols))


for i in range(sig_rows):
    for j in range(sig_cols):
        if sigma_matrix[i][j] != 0:
            z[i][j] = float(1/sigma_matrix[i][j].real)


#print('************************  X Transpose ***********************************')
#print(x_transpose)

print('************************  Y Transpose ***********************************')
#print(y_transpose)
temp = np.matmul(y_transpose, z)
u_matrix = np.matmul(temp, x_transpose)#y_transpose@pseudo_square_matrix@x_transpose

print('************************  U Matrix  ***********************************')
print(u_matrix)

temp2 = np.matmul(c_matrix_np, u_matrix)
final_cur = np.matmul(temp2, r_matrix_np)

print('************************  Final CUR Matrix  ***********************************')

print(np.array(final_cur))

print('************************  A - CUR Matrix ***********************************')

diff_matrix = final_matrix - final_cur
print(diff_matrix)

sum = 0

for i in range(no_of_users):
    for j in range(no_of_movies):
            if diff_matrix.item(i, j) != 0:
                sum += diff_matrix.item(i, j) * diff_matrix.item(i, j)

rmse = np.sqrt(sum/(no_of_users*no_of_movies))

print('Rmse = ', rmse)
print('Time in seconds = ', time.time()-start_time)



