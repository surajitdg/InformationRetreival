import csv
import pickle
import numpy
from movies import Movies, Ratings
from csvreader import save_list_object
from scipy import spatial,stats
from copy import copy


movie_num=int(input("Give Movie Number: "))
movie_num-=1
user_num=int(input("Give User Number: "))
user_num-=1

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


'''with open('objects/matrix.pkl', 'rb') as input:
    load_matrix = pickle.load(input)

with open('objects/movie_mapper.pkl', 'rb') as input:
    movie_id_mapper = pickle.load(input)


record_counter = 0

for i in range(no_of_users):
    for j in range(no_of_movies):
        if load_matrix[i][j] != 0:
            record_counter += 1

#Dumped to csv file for testing#      
with open("test.csv", "w+") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(load_matrix)





                                                            #Collaborative Filtering Approach#

                                                            




load_matrix=numpy.transpose(load_matrix) #For item-item filtering

'''


#test matrix#
example_matrix=[[1,0,3,0,0,5,0,0,5,0,4,0],[0,0,5,4,0,0,4,0,0,2,1,3],[2,4,0,1,2,0,3,0,4,3,5,0],[0,2,4,0,5,0,0,4,0,0,2,0],[0,0,4,3,4,2,0,0,0,0,2,5],[1,0,3,0,3,0,0,2,0,0,4,0]]

load_matrix=example_matrix




load_matrix=numpy.asarray(load_matrix)
if not load_matrix[movie_num][user_num] ==0:
    rating=load_matrix[movie_num][user_num]
    print(rating)
else:
    avg_ratings=[]
    avg_ratings=stats.mstats.tmean(load_matrix, limits=(0,None), inclusive=(False, False), axis=1)   #stores row wise avg ratings in array
    

    dup_matrix=copy(load_matrix)
     

    movie_similarity=[]

    for i in range(0,load_matrix.shape[0]):        
        for j in range(0,load_matrix.shape[1]):       #.shape[1] gives total columns
            if (not(numpy.isnan(load_matrix[i][j])) and not(load_matrix[i][j]) ==0):   # not required,as NaN's are not used in calculation
                load_matrix[i][j] = load_matrix[i][j]-avg_ratings[i] # subracting mean from each row vector
                
                
        numpy.nan_to_num(load_matrix,copy=False)
        movie_similarity.append(1- spatial.distance.cosine(load_matrix[movie_num], load_matrix[i]))



     
    #Taking |N|=2#
    n=0
    similarity_weights={}
    for i in range(0,len(dup_matrix)):
        if(n<=2):
            if(movie_similarity[i]>0):
                similarity_weights[movie_similarity[i]]=dup_matrix[i][user_num]
                n+=1
        else:
            break
    del similarity_weights[1.0]       #Delete own value i.e 1.0 from dict



    #Prediction by taking weighted average#
    rating_numerator=0
    rating_denominator=0
    for key,value in similarity_weights.items():
        rating_numerator+=(key*similarity_weights[key])
        rating_denominator+=key


    #Final Rating#
    rating=round((rating_numerator/rating_denominator),1)
    print(rating)
























