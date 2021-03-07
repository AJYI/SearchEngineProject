# from typing import Match
# from urllib.parse import urlparse
# import spacy	
# spacy_nlp = spacy.load('en_core_web_sm')
import numpy as np
import math
from collections import Counter
from tokenizer import Tokenizer
from numpy import append, dot
from numpy.linalg import norm
from collections import OrderedDict
# from pprint import pprint
import pymongo
from pymongo import MongoClient
# from bson.objectid import ObjectId

# retrieve information from mongoDB
myclient = MongoClient("mongodb://localhost:27017/")
# db = myclient['CS121_norm_100']
db = myclient['CS121_norm_1000']

tokenObj = Tokenizer()

"""
Print a dictionary
"""
def print_dictionary(cur_dict):
    # helper function to print dictionary
    for key in cur_dict:
        print(key, cur_dict[key])
        
        

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
        {"$limit" : 200 }
        ])
        # print("~~~~~getTopDoc type cursor", type(cursor))

        # combine all docIDs together in one list (there are duplicates)
        cursor_list = list(cursor)
        for doc in cursor_list:
            # print("Printing doc ... ")
            # print(doc)
            # print("~~~~~getTopDoc doc['doc']]", doc['doc'])
            allDoc += [doc['doc']]

        # print("Printing len cursor ... ")
        # print(len(cursor_list))
            
    
    # print(allDoc) # this prints all the document ids in all words
    
    docID_Counter = OrderedDict(Counter(allDoc)) # counts number of docIDs
    # print(docID_Counter.most_common(450)) # this keeps the top 30 
    # docID_Counter = docID_Counter.most_common(200)
    # print(docID_Counter)
    # print(docID_Counter.keys())
    
    return list(docID_Counter.keys())


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
        

if __name__ == "__main__":
    """combine all query_database documents together in a list called allDoc
    counter allDoc    """

    query_list  = ["dragon", "cut"]

    docIDS = getTopDoc(query_list)
    print("docIDS", docIDS)
    # print("\n\nquery_database", query_database)

    doc_normalized = getDocNormal(query_list, docIDS)
    print("\nnoarmlized")
    print_dictionary(doc_normalized)



"""


{query[0]: {cursor for query [0]},
query[1]: {cursor for query [1]},
query[n]: {cursor for query [n]}}

# 100 total doc per word

query_database = {}
for word in query_unique_list: # returns dictionay ! 
    cursor = mycol.aggregate([
        {"$match": {"_id": word}}, # matches with the id = word
        {"$unwind": "$doc_info"}, # it extracts the array ! gets the whole array
        {"$project":{
            "doc": "$doc_info.originalID",
            "tagScore": "$doc_info.tagScore"
        }},
        {"$sort": { "tagScore": pymongo.DESCENDING}}, 
        {"$limit" : 100 }
    ])

    query_database[word] = cursor

combine all query_database documents together in a list called allDoc
counter allDoc 
"""