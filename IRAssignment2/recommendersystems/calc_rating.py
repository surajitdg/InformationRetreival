import numpy
from numpy import dot
from numpy.linalg import norm
from scipy import spatial,stats
from copy import copy
def calculate_cf(load_matrix, movie_num, user_num): #calculate rating based on collaborative filtering
    
    load_matrix=numpy.asarray(load_matrix)

    
    avg_ratings=[]
    avg_ratings=stats.mstats.tmean(load_matrix, limits=(0,None), inclusive=(False, False), axis=1)   #stores row wise avg ratings in array
        
            
    
    dup_matrix=copy(load_matrix)
     
    load_matrix=load_matrix.astype(float)
    
    movie_similarity=[]
    
    
    for i in range(0,load_matrix.shape[0]):        
        for j in range(0,load_matrix.shape[1]):       #.shape[1] gives total columns
            if (not(load_matrix[i][j]) ==0):      # not required,as Zero's are not used in calculation
                
                load_matrix[i][j] -=avg_ratings[i] # subracting mean from each row vector
                        
            
                
        movie_similarity.append(1 - spatial.distance.cosine(load_matrix[movie_num],load_matrix[i]))
    
    
    
    #Taking |N|=2#
    n=0
    similarity_weights={}
    for i in range(0,len(dup_matrix)):
        if(n<2):
            if(movie_similarity[i]>0 and not i == movie_num):
                similarity_weights[movie_similarity[i]]=dup_matrix[i][user_num]
                n+=1
        else:
            break
        

    #Prediction by taking weighted average#
    rating_numerator=0
    rating_denominator=0
    for key,value in similarity_weights.items():
        rating_numerator+=(key*similarity_weights[key])
        rating_denominator+=key


    #Final Rating#
    rating=round((rating_numerator/rating_denominator),1)
    if rating<=0:
        rating=1
    if rating>5:
        rating=5
    return rating


def calculate_cfbl(load_matrix, movie_num, user_num):   #calculate rating based on cf with baseline approach
    
    load_matrix=numpy.asarray(load_matrix)

    
    avg_ratings=[]
    avg_ratings=stats.mstats.tmean(load_matrix, limits=(0,None), inclusive=(False, False), axis=1)   #stores row wise avg ratings in array
        
            
    
    dup_matrix=copy(load_matrix)
     
    load_matrix=load_matrix.astype(float)
    
    movie_similarity=[]
    
    
    for i in range(0,load_matrix.shape[0]):        
        for j in range(0,load_matrix.shape[1]):       #.shape[1] gives total columns
            if (not(load_matrix[i][j]) ==0):      # not required,as Zero's are not used in calculation
                
                load_matrix[i][j] -=avg_ratings[i] # subracting mean from each row vector
                        
            
                
        movie_similarity.append(1 - spatial.distance.cosine(load_matrix[movie_num],load_matrix[i]))
    
    
    
    #Taking |N|=2#
    n=0
    similarity_weights={}
    u=stats.mstats.tmean(dup_matrix, limits=(0,None), inclusive=(False, False), axis=None)   #u is the mean of all the ratings in the given matrix
    temp1=copy(dup_matrix)
    temp1=numpy.transpose(temp1)
    bx=(stats.mstats.tmean(temp1[user_num], limits=(0,None), inclusive=(False, False), axis=None))-u   #calculate bx for the given user
    bxj=[]
    for i in range(0,len(dup_matrix)):
        if(n<2):
            if(movie_similarity[i]>0 and not i == movie_num):
                similarity_weights[movie_similarity[i]]=dup_matrix[i][user_num]
                n+=1
                bxj.append(u+bx+((stats.mstats.tmean(dup_matrix[i], limits=(0,None), inclusive=(False, False), axis=None))-u))  #calculate each bxj
        else:
            break

    
    #Prediction by taking weighted average#   
    bi=(stats.mstats.tmean(dup_matrix[movie_num], limits=(0,None), inclusive=(False, False), axis=None))-u  #calculate bi for all items 
    bxi=u+bx+bi     #calculate bxi
    rating_numerator=0
    rating_denominator=0
    j=0
    
    for key,value in similarity_weights.items():
        rating_numerator+=(key*(similarity_weights[key]-bxj[j]))
        rating_denominator+=key
        j+=1


    #Final Rating#
    rating=bxi+round((rating_numerator/rating_denominator),2)
    if rating<=0:
        rating=1
    if rating>5:
        rating=5
    return rating





