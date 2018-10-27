import csv
import pickle
from movies import Movies, Ratings
from utilityfunctions import read_csv, save_list_object


movie_list = []
rating_list_base = []
rating_list_test = []


movie_list = read_csv('dataset/test100/movies.csv', movie_list, Movies)
rating_list_base = read_csv('dataset/test100/ratings1_base.csv', rating_list_base, Ratings)
rating_list_test = read_csv('dataset/test100/ratings1_test.csv', rating_list_test, Ratings)


save_list_object(movie_list, 'objects/test100/movie_list.pkl')
save_list_object(rating_list_base, 'objects/test100/rating_list_base.pkl')
save_list_object(rating_list_test, 'objects/test100/rating_list_test.pkl')



