import svd_recommender
import pandas as pd
import numpy as nm
from svd_recommender import predicted_matrix
from svd_recommender import calculate_rmse
from svd_recommender import spearman_rank_correlation
from svd_recommender import precision_at_top
from svd_recommender import svd_with_ninty_percent_energy

#main file to find error rates
# for svd normal,assume concepts as 200
#change pathname as local directory
pathname_base = "/home/hellstar/Desktop/Programs/ml-latest-small/base_matrix.csv"
pathname_test = "/home/hellstar/Desktop/Programs/ml-latest-small/test_matrix.csv"
ratings = pd.read_csv(pathname_base,sep=",")
ratings_array = ratings.as_matrix()
test = pd.read_csv(pathname_test,sep=",")
test_array = test.as_matrix()

#find predicted matrix using svd
concepts = min(ratings_array.shape[0],ratings_array.shape[1])-2
p,e = predicted_matrix (ratings_array,200)

total_array = test_array+ratings_array # total array contains test as well as base arrays

#calculate rmse
rmse = calculate_rmse(total_array,p)
print("Rmse for svd = ",rmse)

#calculate spearman correlation
scc = spearman_rank_correlation(total_array,p)
print("Spearman rank correlation = ",scc)

#calculate precision at top k,set k and userid
k = 1682
userid = 30
pat = precision_at_top(total_array,p,10,30)
print("Precision at top = ",pat)

# svd with 90 % energy
p1,e1 = svd_with_ninty_percent_energy(ratings_array,concepts)

print("-------SVD with 90% energy case--------")

#calculate rmse
rmse = calculate_rmse(total_array,p1)
print("Rmse for svd = ",rmse)

#calculate spearman correlation
scc = spearman_rank_correlation(total_array,p1)
print("Spearman rank correlation = ",scc)

#calculate precision at top k,set k and userid
k = 1682
userid = 30
pat = precision_at_top(total_array,p1,10,30)
print("Precision at top = ",pat)