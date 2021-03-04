from urllib.parse import urlparse
import spacy	
spacy_nlp = spacy.load('en_core_web_sm')
import numpy as np
import math
import collections
from tokenizer import Tokenizer
from numpy import append, dot
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
db = myclient['CS121_norm_1000']
tokenObj = Tokenizer()


def print_dict(cur_dict):
    # helper function 
    for key in cur_dict:
        print(key, cur_dict[key])


def get_query_vector(user_input):
    """
    for the query vector, normalizes and returns vector
    param : user_input | list
    returns : np.array(vector_list), user_input_unique
    """
    print(user_input)
    # [alice fly faustina flys]
    # [alice fly faustina fly]
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
    param : query | string , tfwt | int
    returns : query_weight | float
    """
    # text first char in query
    first_letter = query[0]

    # this is text[0]
    alpha_db = db[first_letter]
    # df = alpha_db.find_one({"_id":query})['total']
    idf = alpha_db.find_one({"_id":query})['idf']
    # print("total of", query, ": ", df)

    ## according to the db! ##
    # total_amt_doc = 100 
    ## according to the db! ##

    # idf = math.log(total_amt_doc/df)
    # print("get_query_weight total_amt_doc :", total_amt_doc)
    print("get_query_weight tfwt :", tfwt)
    # print("get_query_weight df :", df)
    print("get_query_weight idf", idf)
    weight = tfwt * idf 
    print("get_query_weight's weight : ", weight)

    return weight



def document_weight_tag(user_input_unique_list):
    """
    for the query normalized values  
    param : user_input_unique | string 
    returns : doc_dic | string
    """
    word_doc_dict = {}
    # {query_word : docdictionay, query_word : docdictionay}
    docid_list = [[],[]]

    # if the query is 2 words only
    if len(user_input_unique_list) == 2:

        # for query_word in user_input_unique_list:
        for i in range(len(user_input_unique_list)):
            # doc_dic = {origianlId : [normalized, tagscore]}
            # doc_tag_noarmald = key = tagscore : value docid_list = []
            # doc_tag_noarmal = {}
            # if tagscore is not in doc_tag_noarmal.keys():
            #     add into doc_tag_noarmal[tagscore] = docid
            # else:
            #     doc_tag_noarmal[tagscore] add into list of docid_list

            # sort dictionay with key (tagscore):
            # we get top 30 ->

            doc_dict = {}

            first_letter = user_input_unique_list[i][0]
            alpha_db = db[first_letter]
            docinfo = alpha_db.find_one({"_id":user_input_unique_list[i]})['doc_info'] 

            # each word willl have a doc_dict 
            for document in docinfo:
                doc_dict[document['originalID']] = [document['normalized'], document['tagScore']] # [normalized, tagsore]
                docid_list[i].append(document['originalID'])
            
            word_doc_dict[user_input_unique_list[i]] = doc_dict
        
        print_dict(word_doc_dict)

        # docid that contains both words 
        unique_id = set(docid_list[0]).intersection(set(docid_list[1]))
        # word_doc_dict : {query_word : {origianlId : [normalized, tagscore]}, query_word : {origianlId : [normalized, tagscore]}}
        # access all the document objects for 1 term
        
        # Faustina Code
        # counter = 0
        # minTagscore = 0
        # topTagScore = []
        # for i in range(len(user_input_unique_list)): 
        #     # for every document in the query[i] (a word)   
        #     for currDoc in word_doc_dict[user_input_unique_list[i]]:
        #         currTagScore = word_doc_dict[user_input_unique_list[i]][currDoc][1]
        #         if counter == 0:
        #             # intialize minimum tag score / doc associated with minTagScore
        #             minTagScore = word_doc_dict[user_input_unique_list[i]][currDoc][1]
        #             minDoc = currDoc
                
        #         if counter > 30:
        #             if currTagScore >= minTagScore:
                        

            
            # print(f"i = {i}")
            # print(word_doc_dict[user_input_unique_list[i]])

        # for word_doc in word_doc_dict:
        #     docdictionay = word_doc_dict[word_doc]
                
        
        # for word_doc in word_doc_dict:
        #     doc_dictionay = word_doc_dict[word_doc] # {origianlId : [normalized, tagscore]}
        #     for norm_tag in doc_dictionay:
        #         tag = norm_tag[1] # tag importance

    # return doc_dict


document_weight_tag(['fully','connectivity'])


def document_weight(one_word):
    """
    for the query normalized values  
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


def document_weight_muliple(user_input_unique):
    """
    for the query weight for multiple
    param : user_input_unique | list string 
    returns : doc_dic | doc_dic
    """
    doc_dic = {}

    idx_user_input = len(user_input_unique)

    d_dict_list = [] # all document dictioniees in list key:normalized
    # we have to keep track of the  which word accordings to the normzlaied .
    # we need to put it in a double array, x=documents y=terms
    # user_input_unique[]
    
    for i in range(idx_user_input):
        # retrive all document in all quries 
        doc_dict = document_weight(user_input_unique[i]) # asumming top 30 tag_imp here 
        d_dict_list.append(doc_dict) # asumming top 30 tag_imp

    cosine_sim_list = [] # list of cosine sim of each doc & query 
    # q_vec = []
    # cosine_sim_list = cosine_similarity(q_vec, d_dict_list)

    return cosine_sim_list


# i was gonna json file according to each uniquedocid,

# doc_vect = [doc2[normlized] , doc2[normalzied]]
def cosine_similarity(q_vec, d_dict):
    """
    commputes cosine similarity for one word
    param : q_vec|np array, d_vec| list of list
    return : list | cos_sim_list
    """
    cos_sim_list = []

    # example cut 
    # {3: 0.23201859645566503, 39: 0.08625382108082906}
    for doc in d_dict:
        # doc product of q_vec & 
        d_vec = np.array(d_dict[doc])
        cos_sim = np.dot(d_vec, q_vec)
        cos_sim_list.append(cos_sim)

    cos_sim_list.sort(reverse=True)

    if (len(cos_sim_list) > 20 ):
        cos_sim_list = cos_sim_list[:20]
    
    return cos_sim_list


# def compute_score(cos_sim_list):
#     score_list = []

#     for cos_sim in cos_sim_list: # one doc
#         score = #add all oof them 


# # doc_vect = [doc2[normlized] , doc2[normalzied]]
# def cosine_similarity(q_vec, d_dict, user_input_unique):
#     """
#     commputes cosine similarity 
#     param : q_vec|np array, d_vec| list of list, user_input_unique
#     return : list | cos_sim_list
#     """
#     cos_sim_list = []

#     if len(user_input_unique) == 1: 
#         # example cut 
#         # {3: 0.23201859645566503, 39: 0.08625382108082906}
#         for doc in d_dict:
#             # doc product of q_vec & 
#             # https://stackoverflow.com/questions/18424228/cosine-similarity-between-2-number-lists
#             d_vec = np.array(d_dict[doc])
#             cos_sim = np.dot(d_vec, q_vec)
#             cos_sim_list.append(cos_sim)

#     cos_sim_list.sort(reverse=True)

#     if (len(cos_sim_list) > 20 ):
#         cos_sim_list = cos_sim_list[:20]
    
#     return cos_sim_list
    

"""
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
cos_sim_list = cosine_similarity(q_vec, doc_dict, unique_list)
print("cos sim list : ", cos_sim_list)
"""


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
