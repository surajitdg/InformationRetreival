import numpy as np
import math
import random
from svd_recommender import svd, svd_with_ninty_percent_energy, precision_at_top
import time
from utilityfunctions import read_object

def cur_create(flag):
    total_square = 0.0

    start_time = time.time()
    base_matrix = read_object('objects/test100/base_matrix.pkl')
    test_matrix = read_object('objects/test100/test_matrix.pkl')

    #base_matrix = np.array([[1, 1, 1, 0, 0], [3, 3, 3, 0, 0], [4, 4, 4, 0, 0], [5, 5, 5, 0, 0], [0, 0, 0, 4, 4],
    #                       [0, 0, 0, 5, 5], [0, 0, 0, 2, 2]])

    base_matrix = np.array([np.array(row) for row in base_matrix])
    #base_matrix = np.matrix(base_array)

    test_matrix = np.array([np.array(row) for row in test_matrix])
    #test_matrix = np.matrix(test_array)

    final_matrix = base_matrix + test_matrix

    no_of_users = len(base_matrix)
    no_of_movies = len(base_matrix[0])

    for i in range(no_of_users):
        for j in range(no_of_movies):
            total_square += base_matrix[i][j]*base_matrix[i][j]

    pr_rows = np.zeros(no_of_users)
    pr_cols = np.zeros(no_of_movies)

    for i in range(no_of_users):
        row_sum = 0.0
        for j in range(no_of_movies):
            row_sum += base_matrix[i][j]*base_matrix[i][j]
        pr_rows[i] = row_sum/total_square

    for i in range(no_of_movies):
        col_sum = 0.0
        for j in range(no_of_users):
            col_sum += base_matrix[j][i]*base_matrix[j][i]
        pr_cols[i] = col_sum/total_square

    ran_rows = []
    ran_cols = []

    r = int(np.linalg.matrix_rank(base_matrix)*0.7)

    for i in range(r):
        ran_rows.append(random.choices(list(range(0, no_of_users)), pr_rows)[0])
        ran_cols.append(random.choices(list(range(0, no_of_movies)), pr_cols)[0])

    px_row = []
    px_col = []

    for i in ran_rows:
        px_row.append(pr_rows[i])

    for i in ran_cols:
        px_col.append(pr_cols[i])

    #ran_rows=[4, 1]
    #ran_cols=[1, 4]

    px_row = np.array(px_row)
    ran_rows = np.array(ran_rows)
    ind = px_row.argsort()[::-1]
    px_row = px_row[ind]
    ran_rows = ran_rows[ind]

    px_col = np.array(px_col)
    ran_cols = np.array(ran_cols)
    ind2 = px_col.argsort()[::-1]
    px_col = px_col[ind2]
    ran_cols = ran_cols[ind2]

    '''print(ran_rows)
    print(px_row)
    print(ran_cols)
    print(px_col)'''

    c_matrix = np.zeros(shape=(no_of_users, r))
    r_matrix = np.zeros(shape=(r, no_of_movies))
    w_matrix = np.zeros(shape=(r, r))
    u_matrix = np.zeros(shape=(r, r))

    count = 0
    for i in ran_cols:
        for j in range(no_of_users):
            c_matrix[j][count] = base_matrix[j][i]*1.0/math.sqrt(r*pr_cols[i])
        count += 1

    count = 0
    for i in ran_rows:
        for j in range(no_of_movies):
            r_matrix[count][j] = base_matrix[i][j]*1.0/math.sqrt(r*pr_rows[i])
        count += 1

    for i in range(len(ran_rows)):
        for j in range(len(ran_cols)):
            w_matrix[i][j] = base_matrix[ran_rows[i]][ran_cols[j]]

    print('************************  C - Matrix  ***********************************')
    print(c_matrix)
    print('************************  R - Matrix  ***********************************')
    print(r_matrix)
    print('************************  W - Matrix  ***********************************')
    print(w_matrix)

    if flag == 0:
        x_matrix, y_matrix, z_matrix = svd(w_matrix, r)
    elif flag == 1:
        a, b, svd_obj = svd_with_ninty_percent_energy(w_matrix, r)
        x_matrix = svd_obj[0]
        z_matrix = svd_obj[1]
        y_matrix = svd_obj[2]

    z_new = np.zeros(shape=(len(z_matrix), len(z_matrix)))

    for i in range(len(z_matrix)):
        if z_matrix[i][i] != 0:
            z_new[i][i] = 1.0/z_matrix[i][i]

    temp_prod = np.matmul(y_matrix, z_new)
    u_matrix = np.matmul(temp_prod, x_matrix.T)

    print('************************  Y - Matrix  ***********************************')
    print(y_matrix)
    print('************************  Z - Matrix  ***********************************')
    print(z_new)
    print('************************  X.T - Matrix  ***********************************')
    print(x_matrix.T)
    print('************************  U - Matrix  ***********************************')
    print(u_matrix)

    temp_prod2 = np.matmul(c_matrix, u_matrix)
    final_cur = np.matmul(temp_prod2, r_matrix)

    print('************************  CUR - Matrix  ***********************************')
    print(final_cur)

    diff_matrix = np.subtract(final_matrix, final_cur)

    print('************************  Base + Test - CUR - Matrix  ***********************************')
    print(diff_matrix)

    diff_calc = 0
    n = no_of_users*no_of_movies
    for i in range(no_of_users):
        for j in range(no_of_movies):
            diff_calc += diff_matrix[i][j]*diff_matrix[i][j]

    rmse_value = np.sqrt(diff_calc/(n))
    pearson = 1 - (6*diff_calc/(n*(n*n - 1)))
    precision = precision_at_top(final_matrix, final_cur, 100, ran_rows[16])
    print('RMSE Value = ', rmse_value)
    print('Pearson = ', pearson)
    print('Precision = ', precision)
    print('Time taken = ', time.time() - start_time)

cur_create(0)
cur_create(1)