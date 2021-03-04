from urllib.parse import urlparse
import spacy	
spacy_nlp = spacy.load('en_core_web_sm')
import numpy as np
import math
import collections
from tokenizer import Tokenizer
from numpy import dot
from numpy.linalg import norm

# ## lemitize
# def lemmatize(sentence):
#     # now using spacy
#     doc = spacy_nlp(sentence)
#     return " ".join([token.lemma_ for token in doc])

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

### working getting information on DB c


myclient = MongoClient("mongodb://localhost:27017/")
db = myclient['CS121_norm_100']
tokenObj = Tokenizer()


def print_dict(cur_dict):
    # helper function 
    for key in cur_dict:
        print(key, cur_dict[key])


# def get_token_tfidf(db, token): 
#     """
#     Looks for the token in the db and returns dictionay
#     return : dict - { docid : tfidf ... }
#     """
#     db_dict = {}
#     # text first char in token
#     first_letter = token[0]
#     # this is text[0]
#     alpha_db = db[first_letter]
#     doc_info = alpha_db.find_one({"_id":token})['doc_info']

#     # getting all the doc info
#     for doc in doc_info:
#         db_dict[doc['uniqueID']] = doc['tf-idf']
#         # print(doc['uniqueID'], doc['tf-idf'])

#     return db_dict


# def get_w_tfidf(token_dict):
#     """
#     Computes the normalized tfidf by dividing with query lengh
#     return : dict | { docid : w_tfidf ... } 
#     """
#     query_len = 0
    
#     for key in token_dict:
#         query_len = token_dict[key]**2
#     query_len = math.sqrt(query_len)

#     for key in token_dict:
#         token_dict[key] = token_dict[key]/query_len

#     return token_dict


def get_query_vector(user_input):
    """
    for the query vector, normalizes and returns vector
    param : user_input | list
    returns : np.array(vector_list), user_input_unique
    """
    print(user_input)
    user_list = tokenObj.tokenize(user_input) # assume not a unique words allows dupe
    input_freq_dict = collections.Counter(user_list) ## assume its returning term tf weight 
    
    query_len = 0
    user_input_unique = [] # keep track of the query vec word order
    normalized_list = []


    ## calculate tf weight 
    print("Start calculate tf weight")
    print(input_freq_dict)
    for key in input_freq_dict:
        tf_weight = get_query_weight(key, input_freq_dict[key])
        print(key , "weight :", tf_weight)
        user_input_unique.append(key)
        normalized_list.append(tf_weight) 
        query_len += tf_weight**2

    print("Input frequecy dictionary")
    print(input_freq_dict)

    print("Normalized list")
    print(normalized_list)

    print("User input unique")
    print(user_input_unique)

    query_len = math.sqrt(query_len)

    vector_list = []

    # normalize
    for item in normalized_list:
        item = item/query_len
        vector_list.append(item)

    return np.array(vector_list), user_input_unique


## before we pass in we get uniqueness && pass 
def get_query_weight(query, tfwt):
    """
    for the query weight 
    param : query | string 
    returns : query_weight | float
    """
    # text first char in query
    first_letter = query[0]

    # this is text[0]
    alpha_db = db[first_letter]
    df = alpha_db.find_one({"_id":query})['total']
    print("total of", query, ": ", df)

    ## according to the db! ##
    total_amt_doc = 100 
    ## according to the db! ##

    # idf = math.log(total_amt_doc/df)
    print("get_query_weight total_amt_doc :", total_amt_doc)
    print("get_query_weight tfwt :", tfwt)
    print("get_query_weight df :", df)
    print("get_query_weight idf", math.log10(total_amt_doc/df))
    weight = tfwt * math.log10(total_amt_doc/df)
    print("get_query_weight's weight : ", weight)
    return weight




def document_weight(one_word):
    """
    for the query weight 
    param : user_input_unique | string 
    returns : doc_dic | string
    """
    doc_dic = {}
    # text first char in query
    first_letter = one_word[0]

    # this is text[0]
    alpha_db = db[first_letter]
    docinfo = alpha_db.find_one({"_id":one_word})['doc_info']
    for obj in docinfo:
        normalized = obj['normalized']
        doc_dic[obj['uniqueID']] = normalized

    return doc_dic

# union_docid = set(d_dict.key()) && set(d_dict.key())
# key = [doc_idunion]: value_normalised=[[d1], [d2], [d3]]


# def document_weight_muliple(user_input_unique):
#     """
#     for the query weight for multiple
#     param : user_input_unique | list string 
#     returns : doc_dic | doc_dic
#     """
#     doc_dic = {}

#     idx_user_input = len(user_input_unique)

#     d_dict_list = [] # all document dictioniees in list key:normalized
#     # we have to keep track of the  which word accordings to the normzlaied .
#     # we need to put it in a double array, x=documents y=terms
#     union_docid = []
    
#     for i in range(idx_user_input):
#         # retrive all document in all quries 
#         doc_dict = document_weight(user_input_unique[i]) 
#         d_dict_list.append(doc_dict)
#         if i == 0:
#             union_docid += doc_dict.keys()
#         else:
#             union_docid = set(set(doc_dict.keys()).union(union_docid))
    
#     for docid in union_docid:
#         for d_dict in d_dict_list:


#     return doc_dic



# doc_vect = [doc2[normlized] , doc2[normalzied]]
def cosine_simlarity(q_vec, d_dict, user_input_unique):
    """
    param : q_vec|np array, d_vec| list of list, user_input_unique
    return : list | cos_sim_list
    """
    cos_sim_list = []

    if len(user_input_unique) == 1: 
        # example cut 
        # {3: 0.23201859645566503, 39: 0.08625382108082906}
        for doc in d_dict:
            # doc product of q_vec & 
            # https://stackoverflow.com/questions/18424228/cosine-similarity-between-2-number-lists
            d_vec = np.array(d_dict[doc])
            cos_sim = np.dot(d_vec, q_vec)
            cos_sim_list.append(cos_sim)

    cos_sim_list.sort(reverse=True)

    if (len(cos_sim_list) > 20 ):
        cos_sim_list = cos_sim_list[:20]
    
    return cos_sim_list
    


enter1 = "cut" # 
enter2 = "cut connectivity" # cut - doc id : 3 & 39 , connectivity - doc id: 3 & 52
enter3 = "cut fully" # cut - doc id : 3 & 39 , fully - doc id: 3 & 7 & 92
enter4 = "fully"

# input_list = tokenObj.tokenize(enter2)
# np.array(vector_list), user_input_unique
user_input = input("Enter : ")
q_vec , unique_list = get_query_vector(user_input)
print("get_query_vector: ", q_vec , unique_list)
doc_dict = document_weight(unique_list)
print("document_weight: ", doc_dict)
cos_sim_list = cosine_simlarity(q_vec, doc_dict, unique_list)
print("cos sim list : ", cos_sim_list)

# ## param : user_input | list of words after the tokenization function
# def serach_query(db, user_input):
#     # how many of tfidf score do we have to retrive
#     # so  we have to atrrive all the keys <- and lengthn them up .. 
#     # if doesnt have the word, we have to initizlie it to zero..

#     no_token = len(user_input)
    
#     if no_token == 0:
#         # we only have to do tfidf one time & compute the quiery lengh once
#         token_dict = get_token_tfidf(db, user_input[0])
#         token_dict = get_w_tfidf(token_dict) # w_tfidf matrix is value
#         print_dict(token_dict)

#     else: # have more than 2 user_input
#         # this is when we have to create matrix 
#         dict_list = [] # storing all the dictionaries in a list
#         # i first run the for loop to retrive the data as i want.. ? 
#         for i in range(0, no_token):
#             # we get tfidf score for all and appends it to the list 
#             dict_list.append(get_token_tfidf(db, user_input[i]))
            
#         # we sort it by the doc id ?.. 
#         doc_list = []
#         # for i in range(1, no_token):
            

#         for item in dict_list:
#             print("\n")
#             print_dict(item)

#     ## after getting the matrix we need to do cosine similary
#     ## and rank according to it 
