from configparser import ConfigParser
from nltk.stem import PorterStemmer
#from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np
import re

numlinks = []
dict_list = []
wiki_url = {}



def init():
    #dict_list = []
    ps = PorterStemmer()

    cfg = ConfigParser()

    cfg.read('static/config.ini')
    numlinks.append(cfg.get('others', 'testlinks'))


    #ignore = cfg.get('others', 'ignoresections')


    for p in range(1, int(numlinks[0])+1):
        term_dict = np.load('tf/tf'+str(p)+'.npy').item()
        dict_list.append(term_dict)
        test_link = 'testlink'
        test_link += str(p)
        #print(test_link)
        wiki_url[p] = cfg.get('links', test_link)
        #print(wiki_url[p])

    i = 0
    for dictionary in dict_list:
        print('Dictionary for doc '+ str(i+1))
        token_list = dictionary.keys()
        for token in token_list:
            print(token+' = '+str(dictionary[token]))
        i += 1


def search(query):
    if(len(dict_list)==0):
        print('Calling init method')
        init()
        print('Numlinks after loading all values = '+str(numlinks))
    #url_list=[]

    ps = PorterStemmer()
    token_list = (query.split())

    doc_frq = 0
    stop_words = set(stopwords.words('english'))
    # Removing whitespaces and special chars#
    tokens = []
    for t in token_list:
        a = t.strip()
        a = re.sub('[^ a-zA-Z0-9]', ' ', a)
        if a not in stop_words:
            tokens.append(ps.stem(a).lower())

    query_weight = []
    i = 0
    for dictionary in dict_list:
        query_weight.append(0)
        for token in tokens:
            if token in dictionary:
                query_weight[i] += dictionary[token][3]
                if dictionary[token][1] == int(numlinks[0]):
                    doc_frq += 1
        i += 1

    doc_frq = int(doc_frq/len(tokens))
    print(len(dict_list))
    print(query_weight)
    #print(wiki_url)
    ranked_links = {}
    print('Length = '+str(len(tokens)))
    print(tokens)
    print(doc_frq)
    print(numlinks[0])
    i = 0
    for links in wiki_url:
        if int(numlinks[0]) == doc_frq or query_weight[i] > 0:
            ranked_links[wiki_url[i+1]] = query_weight[i]
        i += 1
    print(ranked_links)
    sorted_links_desc = []
    ranked_view = [(v, k) for k, v in ranked_links.items()]
    ranked_view.sort(reverse=True)
    for v, k in ranked_view:
        sorted_links_desc.append(k)

    print(sorted_links_desc)
    #ranked_links = sorted(ranked_links.keys(), reverse=True)
    return sorted_links_desc


#init()
#search('Management')

