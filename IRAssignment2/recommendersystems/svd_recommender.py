import pandas as pd
import numpy as nm
import scipy
import math
import operator
import cmath

from scipy.sparse import linalg as ln

def svd(ratings_array,concepts):
    ratings_array_transpose = ratings_array.transpose()
    
   # for nan to 0 conversion,remove if required 
    nm.nan_to_num(ratings_array,copy=False)
    nm.nan_to_num(ratings_array_transpose,copy=False)
    
    # calculating U matrix
    array_product = nm.dot(ratings_array,ratings_array_transpose)
    
    #nm.linalg.eig(array_product) --this is will give issues for large matrix
    eigenvalues,eigenvectors_u = ln.eigs(array_product,k=concepts) #pass concepts or no of eigenvalues req
    
    #sort eigenvalues and eigenvectors
    idx = nm.argsort(-eigenvalues) # for reverse order sorting
    eigenvalues = eigenvalues[idx]
    eigenvectors_u = eigenvectors_u[:,idx]
    
    # calculating V matrix
    array_product2 = nm.dot(ratings_array_transpose,ratings_array) 
    eigenvalues2,eigenvectors_v = ln.eigs(array_product2,k=concepts)
    
    #sort eigenvalues and eigenvectors
    idx1 = nm.argsort(-eigenvalues2) # for reverse order sorting
    eigenvalues2 = eigenvalues2[idx1]
    eigenvectors_v = eigenvectors_v[:,idx1]
    
    # calculating variance matrix
    sigma = nm.zeros(shape=(concepts,concepts))
    #eigenvalues_real = nm.zeros(shape=(concepts,))
    
    #print("len %d",eigenvalues[2])
    #for i in range (0,len(eigenvalues)):
        #igenvalues_real[i] = eigenvalues[i].real
        
    #print("ei %d",eigenvalues_real[2])
    for x in range(0,concepts):
        for y in range(0,concepts):
            if (x==y):
                sigma[x][y] = cmath.sqrt(eigenvalues[x]).real
            
    return eigenvectors_u.real ,eigenvectors_v.real ,sigma


#recommending users (assuming users on y-axis,do reverse if array is transposed)
def ratings_users (ratings_array,concepts,userid):
            u,v,s = svd(ratings_array,concepts)
            
            user = nm.zeros(shape=(1,ratings_array.shape[0]))
            for i in range(0,ratings_array.shape[0]):
                user[0][i] = ratings_array[i][userid]
                
            user_concept = nm.dot(user,u)
            
            return user_concept
     
#recommending movies (assuming movies on x-axis,do reverse if array is transposed)
def ratings_movies (ratings_array,concepts,movieid):
            u,v,s = svd(ratings_array,concepts)
            
            movie = nm.zeros(shape=(1,ratings_array.shape[1]))
            for i in range(0,ratings_array.shape[1]):
                movie[0][i] = ratings_array[movieid][i]
            
            #v_t = v.transpose() not required already transposed
            movie_concept = nm.dot(movie,v)
        
            return movie_concept       

def predicted_matrix (ratings_array,concepts):
    u,v,s = svd(ratings_array,concepts)
    v_t = v.transpose()
    usv_t = nm.linalg.multi_dot([u,s,v_t]) #constructed matrix from u sigma and v transpose
    m = nm.zeros(shape=usv_t.shape) # difference matrix between original and reconstructed matrix
    frob_norm  = 0 # sum of squares of elements of difference matrix
    
    m = ratings_array - usv_t #difference
    
    for i in range(0,m.shape[0]):
        for j in range(0,m.shape[1]):
            frob_norm  = frob_norm+math.pow(m[i][j],2) # sum of squares
    
    rmse = frob_norm/(usv_t.shape[0]*usv_t.shape[1]) # mean of squares
    rmse = math.sqrt(rmse) #square root of mean
    #mse = math.sqrt(((ratings_array-usv_t)**2).mean())
    cur_obj = []
    cur_obj.append(u)
    cur_obj.append(s)
    cur_obj.append(v)
    return usv_t,rmse,cur_obj

# this function checks what percentage energy is retained given two concept size            
def check_energy_retained(ratings_array,concepts,concepts_to_check):
    u,v,s = svd(ratings_array,concepts)
    #u1,v1,s1 = svd(ratings_array,concepts_to_check)
    frob_norm = 0
    frob_norm1 = 0
    energy = 0
    for i in range(0,s.shape[0]):
        for j in range(0,s.shape[1]):
            if (i == j):
                frob_norm = frob_norm+math.pow(s[i][j],2)
                
    for i in range(0,concepts_to_check):
        for j in range(0,concepts_to_check):
            if (i == j):
                frob_norm1 = frob_norm1+math.pow(s[i][j],2)
    
    print("frob norm %d",frob_norm)
    print("frob norm %d",frob_norm1)          
    energy = ((frob_norm -frob_norm1)/frob_norm)*100
    energyretained = (100-energy)
    return energyretained

#this function tries to lower down concept size till 90% energy is retained    
def energy_ninty_percent(ratings_array,concepts):
    u,v,s = svd(ratings_array,concepts)
    eigenvalues = nm.zeros(shape=(1,concepts))
    frob_norm = 0
    for i in range(0,s.shape[0]):
        for j in range(0,s.shape[1]):
            if (i == j):
                eigenvalues[0][j] = s[i][j]
                frob_norm = frob_norm+math.pow(s[i][j],2)
                
    new_concept = lower_concept(eigenvalues,concepts-1,frob_norm,100)   # initially its 100% energy
    #print("we can reduce new concept to is %d",new_concept)
    return new_concept
    
def lower_concept(eigenvalues,concepts,frob_norm,energy):
    frob_norm_current = 0
    if (energy <=90):
        #print("energy is %d",energy)
        return concepts
    
    else:
        for i in range(0,concepts):
                    frob_norm_current = frob_norm_current+math.pow(eigenvalues[0][i],2)
            
    energy = ((frob_norm - frob_norm_current)/frob_norm)*100
    energy= (100-energy)
    #print("energy is %d",energy)
    #print("frob norm is %d",frob_norm)
    #print("frob norm current is %d",frob_norm_current)
    return lower_concept(eigenvalues,concepts-1,frob_norm,energy)    
            

def svd_with_ninty_percent_energy(ratings_array,concepts):
    
    #new concept is returned which retains approx 90% energy
        
        concepts = energy_ninty_percent(ratings_array,concepts) 
    
    #new predicted ratings matrix and rmse is calculated using new concepts
        usv_t,rmse, cur_obj = predicted_matrix(ratings_array,concepts)
    
        return usv_t,rmse, cur_obj

    
                
  # evaluation parameters  rmse with test matrix
def calculate_rmse(test_matrix,predicted_matrix):
     
    m = nm.zeros(shape=predicted_matrix.shape) # difference matrix between original and reconstructed matrix
    frob_norm  = 0 # sum of squares of elements of difference matrix
    
    for i in range(0,predicted_matrix.shape[0]):
        for j in range(0,predicted_matrix.shape[1]):
            m[i][j] = test_matrix[i][j] - predicted_matrix[i][j] #difference
            frob_norm  = frob_norm+math.pow(m[i][j],2) # sum of squares
    
    rmse = frob_norm/(predicted_matrix.shape[0]*predicted_matrix.shape[1]) # mean of squares
    rmse = math.sqrt(rmse) #square root of mean
    return rmse
    
  # evaluation parameters pearson correlation coeffiecient
def spearman_rank_correlation(test_matrix,predicted_matrix):
    m = nm.zeros(shape=predicted_matrix.shape)
    frob_norm = 0 
    
    for i in range (0,predicted_matrix.shape[0]):
        for j in range (0,predicted_matrix.shape[1]):
            m[i][j] = test_matrix[i][j]-predicted_matrix[i][j]
            frob_norm = frob_norm+math.pow(m[i][j],2)
            
    frob_norm  = 6*frob_norm
    n = predicted_matrix.shape[0]*predicted_matrix.shape[1]
    scc = frob_norm/(n*(math.pow(n,2)-1))
    scc = 1-scc
    return scc
    

  # evaluation parameter precision at top k

def precision_at_top(test_matrix,predicted_matrix,k,userid):
    
    # converting to binary model,setting threshold to 1,ratings 
    # above 1 is considered relevant
    thrs = 1
    relevant = {}
    recommended = {}
    rel_recm = [] # relevant & recommended intersection
    top_recommended = 0
    top_relevant = 0
    recommend_list = []
    relevant_list = []
    for j in range(0,predicted_matrix.shape[1]):
                if (top_recommended < k):
                    if (predicted_matrix[userid][j] > thrs):
                        recommended.update({j:predicted_matrix[userid][j]})
                        top_recommended = top_recommended+1
            
                
    recommended = sorted(recommended.items(),key=operator.itemgetter(1),reverse=True)
    for c in range(0,len(recommended)):
                recommend_list.append(recommended[c][0])
            
        
            
    for j in range(0,test_matrix.shape[1]):
        if (j in recommend_list):
            if (test_matrix[userid][j]>thrs):
                relevant_list.append(j)
            
    #for d in range(0,len(relevant)):
        #if (relevant[d][1]>thrs):
                #relevant_list.append(relevant[d][1])
                
    
    rel_recm = set(recommend_list).intersection(relevant_list)
    c_rel_recm = len(rel_recm) # count of intersection
    c_rec = len(recommend_list)
    
    if (c_rec == 0):
        return 0
    else:
        precision = float(c_rel_recm)/c_rec
    
    return precision
    
      
                
    
    
    
    
    
    
    