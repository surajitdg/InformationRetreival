from configparser import ConfigParser
from nltk.stem import PorterStemmer
#from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import re
import math
#import glob
import numpy as np
ps = PorterStemmer()

cfg = ConfigParser()

cfg.read('static/config.ini')
numlinks = cfg.get('others', 'testlinks')
#ignore = cfg.get('others', 'ignoresections')

stopwords = set(stopwords.words('english'))
#special_chars = ["(",")"]

dict_list = []
allunique = []
for p in range(1, int(numlinks)+1):

    wordlist = []
    docName = 'tf'+str(p)+'.csv'
    f = open('testcorpus/doc'+str(p)+'.txt','r')
    doc = f.read()
    token = doc.split()
    

    #Removing whitespaces and special chars#
    tokens = []
    for t in token:
        a = t.strip()
        a = re.sub('[^ a-zA-Z0-9]', ' ', a)
        #a = a.encode('ascii')
        #print(a)
        tokens.append(a)

    #Storing tokens in different files#
    '''data1 = {'Term':tokens}
    token = pd.DataFrame(data1)
    token.to_csv('tokens/doc'+str(p)+'.csv', sep=',')'''

    #Stemming all the words#    
    for w in tokens:
        #w = w.encode('ascii')
        if w not in stopwords:
            wordlist.append(ps.stem(w).lower())

    stemdata = ''
    for wor in wordlist:
        stemdata = stemdata + ' ' + str(wor)



    #file = open('testcorpus/stem/doc' + str(p)+'.txt', 'w+')
    #file.write(stemdata)
    #file.close()


    data2 = {'Term': wordlist}
    words = pd.DataFrame(data2)
    #words.to_csv('tokens/doc' + str(p) + '.csv', sep=',')
            
            
    '''string = ''
    count=0
    for word in wordlist:
                string = string+" "+word
                count += 1
    print(string)
    print(count)'''
    uniquewords = sorted(set(wordlist))
    print('for '+str(p)+' file uniquewords = '+str(len(uniquewords)))

    #.........................................For TF.........................................#
    #Calculating term frequency#
    tf = []
    term_dict = {}
    for token in uniquewords:
        c = wordlist.count(token)/(len(wordlist)*(1.0))
        tf.append(c)
        value_list = [c]
        #value_list.append(c)
        term_dict[token] = value_list

    dict_list.append(term_dict)

    allunique.append(uniquewords)
    
    data = {'Term': uniquewords, 'Frequency' : tf}
    tf_df = pd.DataFrame(data)
    #b = open('H:/SEM 1/IR/Assignments/Assignment 1/IRAssignment1/tfidf/'+docName, 'w+')
    
    #Used to_csv function to save in different csv files
    #tf_df.to_csv('tf/tf'+str(p)+'.csv', sep=',')

    #b.close()
    


    #.........................................For IDF........................................#
    
#Count the number of documents(DF) in which the term is present#
uniquewordset = set()
for uniquewordlist in allunique:
    tempset = sorted(set(uniquewordlist))
    for word in tempset:
        if word not in uniquewordset:
            uniquewordset.add(word)

dict_index = 1
for dictionary in dict_list:
    token_list = dictionary.keys()
    #doc_freq = []

    print("dict_index = "+str(dict_index))
    i = 0
    for token in token_list:
        doc_freq = 0
        inv_doc_freq = 0
        for p in range(1, int(numlinks) + 1):
            docName = 'tf' + str(p) + '.csv'
            f = open('testcorpus/stem/doc' + str(p) + '.txt', 'r')
            doc = f.read()
            # print(doc)
            f.close()
            # print(alluniq)
            if doc.find(str(token)) >= 0:
                doc_freq += 1
        inv_doc_freq = math.log(int(numlinks)/doc_freq*(1.0))
        weight = dictionary[token][0]*inv_doc_freq
        dictionary[token].extend([doc_freq, inv_doc_freq, weight])
        #dictionary[token].append(doc_freq)
        #dictionary[token].append(inv_doc_freq)
        #dictionary[token].append(weight)
        print(token + " = " + str(dictionary[token]))
        #np.save('tf/tf' + str(p)+'.npy', dictionary)
        i += 1
    np.save('tf/tf' + str(dict_index) + '.npy', dictionary)
    dict_index += 1

