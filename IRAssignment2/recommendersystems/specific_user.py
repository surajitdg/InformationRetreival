import calc_rating
import main
from main import load_matrix
import numpy


user_num=int(input("Give User Number: "))
user_num-=1
movie_num=int(input("Give The Number Of Movies To Find Rating For: "))
movie_num
rating=[]
for i in range(0,movie_num):
    if not load_matrix[i][user_num]==0:
        rating.append(load_matrix[i][user_num])
    else:
        rating.append(calc_rating.calculate_cfbl(load_matrix,i,user_num))
print ("Ratings: ",rating)
