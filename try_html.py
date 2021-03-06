from urllib.parse import urlparse
import spacy	
spacy_nlp = spacy.load('en_core_web_sm')
import numpy as np
import math
import collections
from tokenizer import Tokenizer
from numpy import append, dot
from numpy.linalg import norm
from collections import OrderedDict
from pprint import pprint



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




    # doc_dic = {origianlId : [normalized, tagscore]}
    # doc_tag_noarmald = key = tagscore : value docid_list = []
    # doc_tag_noarmal = {}
    # if tagscore is not in doc_tag_noarmal.keys():
    #     add into doc_tag_noarmal[tagscore] = docid
    # else:
    #     doc_tag_noarmal[tagscore] add into list of docid_list

    # sort dictionay with key (tagscore):
    # we get top 30 ->


def document_weight_tag(user_input_unique_list):
    """
    for the query normalized values  
    param : user_input_unique | string 
    returns : doc_dic | string
    """
    word_doc_dict = {}
    # {query_word : docdictionay, query_word : docdictionay}
    docid_list = [[],[]]
    word_doc_tag = {}
    sort_tag_list =  []
    sort_tag_dict = {}

    # if the query is 2 words only
    if len(user_input_unique_list) == 2:
        # for query_word in user_input_unique_list:
        for i in range(len(user_input_unique_list)):
            doc_dict = {}
            doc_tag_norm_dict = {}

            first_letter = user_input_unique_list[i][0]
            alpha_db = db[first_letter]
            docinfo = alpha_db.find_one({"_id":user_input_unique_list[i]})['doc_info'] 

            # each word willl have a doc_dict 
            for document in docinfo:
                # print('word : ',user_input_unique_list[i])
                tagScore = document['tagScore']
                docid = document['originalID']
                doc_dict[document['originalID']] = [document['normalized'], tagScore] # [normalized, tagsore]
                docid_list[i].append(document['originalID'])

                # print("tag : ", tagScore, "tag : ", type(tagScore),"\n")
                if tagScore in doc_tag_norm_dict.keys():
                    # print("tag : ", tagScore, "tag : ", type(tagScore),"already   exist: ", doc_tag_norm_dict[tagScore])
                    doc_tag_norm_dict[tagScore] += [docid]
                    # print("after putting :",  doc_tag_norm_dict[tagScore])
                else:
                    doc_tag_norm_dict[tagScore] = ([docid])
            
            word_doc_dict[user_input_unique_list[i]] = doc_dict
            word_doc_tag[user_input_unique_list[i]] = doc_tag_norm_dict
            # print("sorted tag list: ", sorted(list(doc_tag_norm_dict.keys()), key = lambda x:float(x), reverse=True))
            sort_tag_dict[user_input_unique_list[i]] = sorted(list(doc_tag_norm_dict.keys()), key = lambda x:float(x), reverse=True)
            sort_tag_list.append(sorted(list(doc_tag_norm_dict.keys()), key = lambda x:float(x), reverse=True))
        
        # print_dict(word_doc_dict)
        print("DocTag\n")
        print_dict(word_doc_tag)
        print("Sorted Tag\n")
        print(sort_tag_list)
        # docid that contains both words 
        intersect_ids = set(docid_list[0]).intersection(set(docid_list[1]))
        print("intersetct ids: ", intersect_ids)

        word_list = []
        # word_dict = {}
        # get  unique id list first
        
        for word in  word_doc_dict: # {query_word : docdictionay, query_word : docdictionay}
            if len(intersect_ids) > 30:
                print("~~~~~~In > len(intersect_ids) > 30")
                counter = 0
                word_dict = {}

                # for tag_score in sort_tag_list:
                for tag_score in sort_tag_dict[word]:
                    print("sort_tag_dict[word]", sort_tag_dict[word])
                    print("\n\n!!tagscore: ", tag_score)
                    # print
                    # for tag in tag_score:
                    print("!!list of doc id : ", tag_score)
                    print('word_doc_tag keys',word_doc_tag.keys())
                    print('accessing ', word)
                    # print("The dictionay for",word,":" , word_doc_tag[word])
                    dictionay = word_doc_tag[word]
                    print("!!list of word doc tag id : ", dictionay[tag_score])
                    list_of_doc_id = dictionay[tag_score]
                    no_docid = len(list_of_doc_id)

                    if counter < 30:
                        print("~~~~~~~~In if counter < 30")
                        counter += no_docid
                        print("Adding len of doc id", no_docid)

                        # we add 
                        for docid in list_of_doc_id:
                            temp_dict = word_doc_dict[word]
                            word_dict[docid] = temp_dict[docid] # [normalized, tagsore]
                            print("Adding", temp_dict[docid], "....")
                    
                    elif counter >=30:
                        print("~~~~~~~~In if counter >= 30")
                        break

                    print("Counter : ", counter)
                        
                word_list.append(word_dict)

            else:
                print("~~~~~~In > len(intersect_ids) < 30")
                word_dict = {}
                # {query_word : docdictionay, query_word : docdictionay}
                # docdictionary ={docid : [normalized, tagsore]}
                # append everything
                for ids in intersect_ids:
                    # print("each ids :", ids)
                    word_dict[ids] = word_doc_dict[word][ids] # [normalized, tagsore]
                    # print("[normalized, tagsore] :", word_doc_dict[word][ids])
                word_list.append(word_dict)


        print("\n\n\nEnding ... \nWord List1 : ", print_dict(word_list[0])) 
        print("\nWord List2 : ", print_dict(word_list[1]))
    # return doc_dict


# document_weight_tag(['computer','irvine'])


def document_weight_tag_limit30(db, user_input_unique_list):
    # for i in range(len(user_input_unique_list)):
    #         doc_dict = {}
    #         doc_tag_norm_dict = {}

    #         first_letter = user_input_unique_list[i][0]
    first_word = user_input_unique_list[0]
    first_letter = first_word[0]
    mycol = db[first_letter] # collection db
    # cursor = mycol.find({'_id':first_word})
    # cursor = mycol.find({'_id':first_word}, {'doc_info': {'originalID': '0/100'}  } )
    # cursor = mycol.find({"_id":first_word}, {"doc_info.originallID" : "0/100"} )

    # cursor = mycol.find({'_id':first_word}, {'doc_info.originalID':'0/100' } )
    # cursor = mycol.find({'_id':first_word}, {'doc_info.originalID'} )
    query =  {"doc_info.originallID" : "0/100"}
    query1 = {'originalID': '1/51'}

    # cursor = mycol.find({"_id": first_word}, {"doc_info":0}) # _id, schooll, idf, total
    # cursor = mycol.find({"_id":first_word},{"doc_info":-1}) # _id, doc_info


    # cursor = mycol.find({"_id":first_word}, {'doc_info': query1})
    # cursor = mycol.find({"_id":first_word}, {"doc_info.originalID"})

    # cursor = mycol.find({"_id":first_word}, {"doc_info.originalID"}, {"doc_info.tagScore"})
    # cursor = mycol.find({"_id":first_word}, {"doc_info.originalID":"0/100"})
    #cursor = mycol.find({"_id":"cut"}, {"doc_info.originalID", "doc_info.tagScore"})

    cursor = mycol.aggregate([
            {"$unwind": "$doc_info"},
            {"$match": {"_id": first_word}},
            {"$project":{
                "doc": "$doc_info.originalID",
                "tagScore": "$doc_info.tagScore"
            }},
            {"$sort": { "tagScore": pymongo.DESCENDING}},
            {"$limit": 30}
        ])
    
    
    



    # cursor = mycol.find({"_id":"cut"}, {"doc_info"})
    # print(cursor.count())
    # print("Pretty print cursor ...")
    # print(cursor.pretty())

    print("Printing cursor ... ")
    # print the cursor
    for doc in cursor:
       pprint(doc)
    print()

document_weight_tag_limit30(db, ["cut"])


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
