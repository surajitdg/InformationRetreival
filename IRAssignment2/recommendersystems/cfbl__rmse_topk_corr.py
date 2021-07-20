import calc_rating
import main
from main import load_matrix,test_matrix
import numpy
import collections


#------------------#Root Mean Square Error#------------------#

#create test set#
'''a,b=10,10
test_matrix=a*[b*[0]]
test_matrix=numpy.asarray(test_matrix)

for i in range(0,a):
    for j in range(0,b):
        if not load_matrix[i][j]==0:
            test_matrix[i][j]=load_matrix[i][j]
'''


#predict non-empty records in test set#
a,b=10,10
new_matrix=a*[b*[0]]
new_matrix=numpy.asarray(new_matrix)
new_matrix=new_matrix.astype(float)
for i in range(0,a):
    for j in range(0,b):
        if not test_matrix[i][j]==0:
            new_matrix[i][j]=round(calc_rating.calculate_cfbl(load_matrix, i, j),1)
  

diff_squares=[]
for i in range(0,a):
    for j in range(0,b):
        if not test_matrix[i][j]==0:
            diff=new_matrix[i][j]-test_matrix[i][j]  #take difference
            diff_squares.append(diff*diff)      #take square of differences

mean=numpy.mean(diff_squares)       #take mean of squares
rmse=round(numpy.sqrt(mean),3)           #take root of mean

print("RMSE w.r.t Test Set: ",rmse)



        

#--------------------#Precision At Top K#---------------------#


k=int(input("Give K: "))
dic={}
for i in range(0,a):
    for j in range(0,b):
        if not new_matrix[i][j]==0:
            dic[new_matrix[i][j]]=test_matrix[i][j]
     
od=collections.OrderedDict(sorted(dic.items(),reverse=True))        #Store array in decreasing ordered dictionary based on predicted ratings


#Relevent Items At k#

thr=3   #Let Threshold rating be 3
relevant=[]
s=0
for key, value in od.items():             #calculate number of relevent items from test matrix
    if s<k:
        if value>=thr:
            relevant.append(value)
            s+=1
num_relevant=len(relevant)
print("relevant: ",relevant)


#Recommended Items At k#

recommend=[]
r=0
for key, value in od.items():             #calculate number of recommended items from predicted matrix
    if r<k:
        if key>=thr:
            recommend.append(key)
            r+=1
num_recommend=len(recommend)
print("recommend: ",recommend)

#Find Intersection Between Both#

num_inter=len(numpy.intersect1d(relevant, recommend, assume_unique=False))

#Find Precision#

precision=num_inter/num_recommend
precision=round(precision*100,2)
print("Precision At Top K: ",precision,"%")



#--------------------#Spearman Rank Correlation#---------------------#
n=len(diff_squares)
rs=1-((6*sum(diff_squares))/(n*(n*n-1)))
print("Spearman's Correlation Coefficient: ",round(rs,2))

