import csv
import pickle
from movies import Movies, Ratings
from csvreader import save_list_object


def get_key(dict_obj, index_value):
    val = list(dict_obj.keys())[list(dict_obj.values()).index(int(index_value))]
    return val


with open('objects/movie_list.pkl', 'rb') as input:
    read_movies_list = pickle.load(input)

#for movie in read_movies_list:
    #print(movie.movie_id, ' ', movie.movie_title, movie.genres)

with open('objects/rating_list.pkl', 'rb') as input:
    read_ratings_list = pickle.load(input)

#for rating in read_ratings_list:
    #print(rating.movie_id, ' ', rating.user_id, rating.rating)

no_of_users = int(read_ratings_list[len(read_ratings_list)-1].user_id)
no_of_movies = int(len(read_movies_list))

'''movie_id_mapper ={}

count = 0
for movie in read_movies_list:
    movie_id_mapper[movie.movie_id] = count
    count += 1

#for key, value in movie_id_mapper.items():
#    print('Key =', key, 'Value = ', value)


#print(no_of_movies, no_of_users)

matrix = []

for i in range(0, no_of_users, 1):
    new_row = []
    for j in range(0, no_of_movies, 1):
        new_row.append(0)
    matrix.append(new_row)


#print(len(matrix), len(matrix[0]))

for rating in read_ratings_list:
        x = int(rating.user_id)
        y = rating.movie_id
        z = int(movie_id_mapper[y])
        #print('Movie id = ', y, 'Index = ', z)
        matrix[x-1][z] = rating.rating

#save_list_object(matrix, 'objects/matrix.pkl')
save_list_object(movie_id_mapper, 'objects/movie_mapper.pkl')'''

#Loading saved matrix and movie mapper dictionary from pickle file#


with open('objects/matrix.pkl', 'rb') as input:
    load_matrix = pickle.load(input)

with open('objects/movie_mapper.pkl', 'rb') as input:
    movie_id_mapper = pickle.load(input)


record_counter = 0

for i in range(no_of_users):
    for j in range(no_of_movies):
        if load_matrix[i][j] != 0:
            print(i, get_key(movie_id_mapper, j), load_matrix[i][j])
            record_counter += 1

print(record_counter)
