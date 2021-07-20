import csv
import pickle
from movies import Movies, Ratings
from csvreader import save_list_object
import numpy as np
from utilityfunctions import read_object, get_key, save_list_object


movies_list = read_object('objects/test100/movie_list.pkl')
ratings_list_base = read_object('objects/test100/rating_list_base.pkl')
ratings_list_test = read_object('objects/test100/rating_list_test.pkl')

no_of_users = int(ratings_list_base[len(ratings_list_base)-1].user_id)
no_of_movies = int(len(movies_list))

movie_id_mapper = {}


count = 0
for movie in movies_list:
    movie_id_mapper[movie.movie_id] = count
    count += 1

base_matrix = []
test_matrix = []

for i in range(0, no_of_users, 1):
    new_row = []
    for j in range(0, no_of_movies, 1):
        new_row.append(0)
    base_matrix.append(new_row)

for base_rating in ratings_list_base:
        x = int(base_rating.user_id)
        y = base_rating.movie_id
        z = int(movie_id_mapper[y])
        #print('Movie id = ', y, 'Index = ', z)
        base_matrix[x-1][z] = float(base_rating.rating)

for i in range(0, no_of_users, 1):
    new_row = []
    for j in range(0, no_of_movies, 1):
        new_row.append(0)
    test_matrix.append(new_row)

for test_rating in ratings_list_test:
        x = int(test_rating.user_id)
        y = test_rating.movie_id
        z = int(movie_id_mapper[y])
        #print('Movie id = ', y, 'Index = ', z)
        test_matrix[x-1][z] = float(test_rating.rating)


save_list_object(base_matrix, 'objects/test100/base_matrix.pkl')
save_list_object(test_matrix, 'objects/test100/test_matrix.pkl')
save_list_object(movie_id_mapper, 'objects/test100/movie_mapper.pkl')

'''

#Loading saved matrix and movie mapper dictionary from pickle file#

load_base_matrix = read_object('objects/test100/base_matrix.pkl')
load_test_matrix = read_object('objects/test100/test_matrix.pkl')
movie_id_mapper = read_object('objects/test100/movie_mapper.pkl')


y = np.array([np.array(row) for row in load_base_matrix])
z = np.array([np.array(row) for row in load_test_matrix])


for i in range(no_of_users):
    for j in range(no_of_movies):
        if int(y[i][j]) != 0:
            print(i+1, get_key(movie_id_mapper, j), y[i][j])

for i in range(no_of_users):
    for j in range(no_of_movies):
        if int(z[i][j]) != 0:
            print(i+1, get_key(movie_id_mapper, j), z[i][j])



'''