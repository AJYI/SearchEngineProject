import numpy as np
import math
from collections import Counter
from tokenizer import Tokenizer
import pymongo
from pymongo import MongoClient
import operator
import json
from bs4 import BeautifulSoup
import os
import re

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
    # 00a0c91e6be4
    # retrieve up to 100 docs (+ its tagScore) for every word in query
    for word in query_list:
        col = word[0]
        # print("Wrod[0]:", word[0])

        if word[0].isdigit():
            col = "Num"
            # print("Is digit changed col:", col)

        cursor = db[col].aggregate([
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

        # combine all docIDs together in one list (there are duplicates)
        cursor_list = list(cursor)
        for doc in cursor_list:
            # print("doc:", doc)
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
            col = word[0]
            # print("Wrod[0]:", word[0])

            if word[0].isdigit():
                col = "Num"
            # print("Is digit changed col:", col)

            # get tag score accordign to the docid & word
            cursor = db[col].aggregate([
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
        col = word[0]
        # print("Wrod[0]:", word[0])

        if word[0].isdigit():
            col = "Num"
            # print("Is digit changed col:", col)

        while counter < 20 and counter < len(docIDs):
            # we look for a matching case
            # getting norm
            cursor = db[col].aggregate([
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
        col = word[0]
        # print("Wrod[0]:", word[0])

        if word[0].isdigit():
            col = "Num"
            # print("Is digit changed col:", col)

        cursor = db[col].aggregate([
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
    docid_list = []
    
    data = json.load(f)
    idx = 1
    for docid in sorted_doc_id_list:
        # print(idx)
        # print(data[docid])
        docid_list.append(data[docid])
        idx += 1
    
    f.close()

    return docid_list


def get_header_descrip(sorted_doc_id_list):
    # print("sorted_doc_id_list")
    title_paragraph = []

    for docid in sorted_doc_id_list:
        htmlFile = os.path.join('WEBPAGES_RAW/', docid)
        if os.path.isfile(htmlFile):
            with open(htmlFile) as fp:
                # soup contains HTML content
                soup = BeautifulSoup(fp, "lxml")

                # get the title
                title = soup.find('title')
                temp_title = ""
                if title is not None:
                    temp_title = title.text
                    temp_title = temp_title.strip()
                else:
                    temp_title = "Title None"
                title.extract()

                # get the content
                body = soup.getText()
                if len(body) != 0:
                    body = re.sub(r"\s+", " ", body)
                    if len(body) > 500:
                        body = body[200:500]

                title_paragraph.append([temp_title, body])

    return title_paragraph
                

def get_result_falsk(user_input):
    """
    For flask to display results
    Parameter: 
        user_input
    Return: url_list
    """
    query_list = tokenObj.tokenize(user_input)
    query_vector = getWordNormal(query_list)
    docIDS = getTopDoc(query_list)
    doc_normalized = getDocNormal(query_list, docIDS)
    sorted_doc_id_list = getCosineSim(query_vector, doc_normalized, query_list, docIDS)
    title_paragraph_list = get_header_descrip(sorted_doc_id_list)
    url_list = get_top20_url(sorted_doc_id_list)
    
    for i in range(len(title_paragraph_list)):
        # print(url_list[i])
        url_list[i] = [url_list[i]] + title_paragraph_list[i]
    # url_list = [url, title, body]

    return url_list


if __name__ == "__main__":
    """combine all query_database documents together in a list called allDoc
    counter allDoc    """

    query = ""
    while query != "quit":
        query = input("\nEnter to search: ")

        if query != "quit":
            print("Befroe token: ", query)
            query_list = tokenObj.tokenize(query)
            print("Query_list")
            print(query_list)
    
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

            title_paragraph_list = get_header_descrip(sorted_doc_id_list)

            # print("\n\nGet_top20_url")
            url_list = get_top20_url(sorted_doc_id_list)

            for i in range(len(title_paragraph_list)):
                # print(url_list[i])
                url_list[i] = [url_list[i]] + title_paragraph_list[i]
                # print(url_list[i])
                
            # print("title_paragraph_list")
            for url in url_list:
                print(url[0])
                print(url[1])
                print(url[2])
                print()

