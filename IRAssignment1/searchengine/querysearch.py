from configparser import ConfigParser
from nltk.stem import PorterStemmer
#from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords as sw
import numpy as np


def init():
    dict_list = []
    ps = PorterStemmer()

    cfg = ConfigParser()

    cfg.read('static/config.ini')
    numlinks = cfg.get('others', 'testlinks')
    #ignore = cfg.get('others', 'ignoresections')

    stopwords = set(sw.words('english'))

    for p in range(1, int(numlinks)+1):
        term_dict = np.load('tf/tf'+str(p)+'.npy').item()
        dict_list.append(term_dict)

    i = 0
    for dictionary in dict_list:
        print('Dictionary for doc '+ str(i+1))
        token_list = dictionary.keys()
        for token in token_list:
            print(token+' = '+str(dictionary[token]))
        i += 1


init()

