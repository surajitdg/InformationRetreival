import csv
import pickle
from movies import Movies, Ratings


def save_list_object(list_obj, file_name):
    with open(file_name, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(list_obj, output, pickle.HIGHEST_PROTOCOL)


movie_list = []
rating_list = []

with open('dataset/test/movies.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        movie_list.append(Movies(row[0], row[1], row[2]))


with open('dataset/test/ratings.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        rating_list.append(Ratings(row[0], row[1], row[2]))


movie_list.pop(0)
rating_list.pop(0)

save_list_object(movie_list, 'objects/movie_list.pkl')
save_list_object(rating_list, 'objects/rating_list.pkl')



