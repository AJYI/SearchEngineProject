import numpy as np
import math
from collections import Counter
from tokenizer import Tokenizer
import pymongo
from pymongo import MongoClient
import operator
import json

# retrieve information from mongoDB
myclient = MongoClient("mongodb://localhost:27017/")
# db = myclient['CS121_norm_100']
db = myclient['CS121DB']

tokenObj = Tokenizer()


def print_dictionary(cur_dict):
    """
    Print a dictionary
    """
    # helper function to print dictionary
    for key in cur_dict:
        print(key, cur_dict[key])
        

"""
Gets the top documents based on the top Counter (overlapping docs)
"""
def getTopDoc(query_list):
    """
    Gets the top 700 documents from each word in the query.
    e.g. If we have 4 word query, we have ~2800 doc in total
    input : query_list | list : query
    return : query_database | dict {query_word : database_list} 
            database_list : list of dict {'_id': quieryword, 'doc': docid, 'tagScore': tagscore, 'norm': normvalue} 
            docID_Counter.keys() | list : overlapping docids among words
    """

    allDoc = []
    SIZE_QUERY = len(query_list)
    
    # retrieve up to 100 docs (+ its tagScore) for every word in query
    for word in query_list:
        cursor = db[word[0]].aggregate([
        {"$match": {"_id": word}}, # matches with the id = word
        {"$unwind": "$doc_info"}, # it extracts the array ! gets the whole array
        {"$project":{
            "doc": "$doc_info.originalID",
            "tagScore": "$doc_info.tagScore",
            "norm": "$doc_info.normalized"
        }},
        {"$sort": { "tagScore": pymongo.DESCENDING}}, 
        {"$limit" : 400 }
        ])
        # print("~~~~~getTopDoc type cursor", type(cursor))

        # combine all docIDs together in one list (there are duplicates)
        cursor_list = list(cursor)
        for doc in cursor_list:
            allDoc += [doc['doc']]
    
    docID_Counter = Counter(allDoc) # counts number of docIDs
    docID_Counter = docID_Counter.most_common() # gets in order 
    docID_Counter = docID_Counter[:50] # gets the top 50
    docID_list = [] # 

    for doc in docID_Counter:
        docID_list.append(doc[0])
    
    # gets top 50 docids in order of tagScore 
    docID_list = getTop50Tag(query_list, docID_list)

    return docID_list


def getTop50Tag(query_list, docid_list):
    """
    get top 50 accordign to the tag
    param : docIDs: top documents with the highest overlap 
    """
    tag_dict = {}  # {docid : totaltag , docid : totaltag ,docid : totaltag 

    for docid in docid_list:
        # lookk thorugh each doc id & calculate tag
        total_tag = 0

        for word in query_list:
            # get tag score accordign to the docid & word
            cursor = db[word[0]].aggregate([
                        {"$unwind": "$doc_info"},
                        {"$match": {"_id": word}},
                        {"$match": {"doc_info.originalID": docid}},
                        {"$project":{
                            "doc": "$doc_info.originalID",
                            "tagScore": "$doc_info.tagScore"
                        }}
                    ])
            
            cursor_list = list(cursor) # changes cursor into a list -> list of dictionaries 

            if (len(cursor_list) == 1):
                # there is a match then add 
                total_tag += cursor_list[0]['tagScore']

        tag_dict[docid] = total_tag # put it in dictionary key = doc :total_tag

    # sort the dictionary accordign to the value 
    tag_dict = sorted(tag_dict.items(), key=operator.itemgetter(1),reverse=True)
    temp_list = [] # temporary list to store docids
    for tuple_item in tag_dict:
        # print(f"{tuple_item[0]} \t {tuple_item[1]}")
        temp_list.append(tuple_item[0])
    
    return temp_list


def getDocNormal(query_list, docIDs):
    """
    Retrieve docID's normalize from mongoDB
    Parameter: 
        query_database: {query[0]: {cursor for query [0]},
                        query[1]: {cursor for query [1]},
                                        ...
                        query[n]: {cursor for query [n]}}
        docIDs: top documents with the highest overlap 
    """    
    # docid : [docid, docid ,docid, docid,docid, docid] overlapping 
    # returns doc_vector : {query_word : [ normalized, 0, ], # if has docid, normalized or 0.  top 20 
    #                query_word : [vector in order of docid]} # noarmlzied 20
    
    #         [docid, docid ,docid, docid, docid]
    # word1 : [norm, norm ,norm, norm, norm, norm]
    # word2 : [norm, norm ,norm, norm, norm, norm]
    # word3 : [norm, norm ,norm, norm, norm, norm]
    # word4 : [norm, norm ,norm, norm, norm, norm]

    # rotate with np

    # print("Matching docids ... ", docIDs)

    doc_vector = {}

    for word in query_list:
        vector_list = []
        counter = 0

        while counter < 20 and counter < len(docIDs):
            # we look for a matching case

            # getting norm
            cursor = db[word[0]].aggregate([
                {"$unwind": "$doc_info"},
                {"$match": {"_id": word}},
                {"$match": {"doc_info.originalID": docIDs[counter]}},
                {"$project":{
                    "doc": "$doc_info.originalID",
                    "norm": "$doc_info.normalized"
                }}
            ])

            cursor_list = list(cursor) # changes cursor into a list -> list of dictionaries 

            if (len(cursor_list) == 1):
                # found a match
                vector_list.append(cursor_list[0]['norm']) # put in a normalized value
            else: 
                # didnt find a match
                vector_list.append(0) # put a 0

            counter += 1
        # print("Resulting vector ... \n", len(vector_list))
        doc_vector[word] = vector_list # each word we return norm vector 
    
    return doc_vector

def getWordNormal(query_list):
    """
    Retrieve docID's normalize from mongoDB
    Parameter: 
        query_list
    """
    query_wt = []
    tfraw_dict = Counter(query_list)
    # {word : freq}
    #  !!!!!  !!!!!  !!!!!  !!!!!  !!!!!   !!!!!  !!!!!  !!!!!  !!!!! 
    n = 37497 #37497 !!!!!   !!!!!  !!!!!   !!!!!  !!!!!  ALEX RUN DB PLZ (cry)
    #  !!!!!  !!!!!  !!!!!  !!!!!  !!!!!   !!!!!  !!!!!  !!!!!  !!!!! 

    for word in query_list:
        # tfraw = tfraw_dict[word] # word's tfraw
        tfwt = 1 + math.log10(tfraw_dict[word])
        
        cursor = db[word[0]].aggregate([
        {"$match": {"_id": word}}, # matches with the id = word
        {"$project":{
            "total": "$total"
        }}
        ])

        cursor_list = list(cursor)

        if (len(cursor_list) == 1): # if we found a match
            # df = cursor_list[0]['total']
            print(word)
            idf = math.log10(n/cursor_list[0]['total'])
            wt = tfwt*idf
            query_wt.append(wt)
        else:
            query_wt.append(0)
        
    query_length = 0
    
    for wt in query_wt:
        query_length += wt**2

    query_length = math.sqrt(query_length)
    
    query_vec = np.true_divide(query_wt, query_length)

    return query_vec

def getCosineSim(query_vec, doc_normalized, query_list, doclist):
    """
    Retrieve docID's normalize from mongoDB
    Parameter: 
        query_vec, doc_normalized, query_list, doclist
    """
    # for word in query_normalized:
    doc_vect = []

    # following the query order 
    for word in query_list:
        # print("doc_normalized[word]")
        # print(doc_normalized[word])
        doc_vect += [doc_normalized[word]]
        # print("doc_vector",doc_vect)

    query_vec = np.array(query_vec)
    doc_vect = np.array(doc_vect)
    doc_vect = doc_vect.T

    # print("\nQuery_vector")
    # print(np.array(query_vec))
    # print("\nDoc_vector")
    # print(np.array(doc_vect))
    
    doc_cossim = {}
    
    idx = 0
    for doc_row in doc_vect:
        doc_cossim[doclist[idx]] = (np.dot(query_vec, doc_row))
        idx += 1

    # print("\nDoc_cossim")
    # print_dictionary(doc_cossim)
    doc_cossim = sorted(doc_cossim.items(), key=operator.itemgetter(1),reverse=True)
    

    sorted_doc_id_list = []
    # print("\nSorted Doc_cossim")
    for tuple_item in doc_cossim:
        # print(f"{tuple_item[0]} \t {tuple_item[1]}")
        sorted_doc_id_list.append(tuple_item[0])
    
    # print(sorted_doc_id_list)
    return sorted_doc_id_list
    

def get_top20_url(sorted_doc_id_list):
    """
    Retrieves the top 20 url from the json file according to the docid
    Parameter: 
        sorted_doc_id_list
    """
    # Opening JSON file 
    f = open("WEBPAGES_RAW/bookkeeping.json",) 
    
    data = json.load(f)
    idx = 1
    for docid in sorted_doc_id_list:
        print(idx)
        print(data[docid])
        idx += 1
    
    f.close() 
                

if __name__ == "__main__":
    """combine all query_database documents together in a list called allDoc
    counter allDoc    """

    query = ""
    while query != "quit":
        query = input("\nEnter to search: ")

        if query != "quit":
            query_list = tokenObj.tokenize(query)
            # print("Query_list")
            # print(query_list)

            # query_list  = ["computer", "science"]
            query_vector = getWordNormal(query_list)
            # print("\n\nWord vector: ")
            # print(query_vector)

            docIDS = getTopDoc(query_list)
            # print("\n\nDoc ids", docIDS)

            doc_normalized = getDocNormal(query_list, docIDS)
            # print("\n\nNoarmlized")
            # print_dictionary(doc_normalized)
            
            # print("\n\nCossim")
            sorted_doc_id_list = getCosineSim(query_vector, doc_normalized, query_list, docIDS)

            print("\n\nGet_top20_url")
            get_top20_url(sorted_doc_id_list)
