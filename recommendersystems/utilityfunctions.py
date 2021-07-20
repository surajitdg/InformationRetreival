import csv
import pickle
from movies import Movies, Ratings


def read_csv(file_name, list_obj, class_obj):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            list_obj.append(class_obj(row[0], row[1], row[2]))
    return list_obj


def save_list_object(list_obj, file_name):
    with open(file_name, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(list_obj, output, pickle.HIGHEST_PROTOCOL)


def get_key(dict_obj, index_value):
    val = list(dict_obj.keys())[list(dict_obj.values()).index(int(index_value))]
    return val


def read_object(filename):
    with open(filename, 'rb') as ip:
        return pickle.load(ip)

