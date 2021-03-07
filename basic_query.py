from tokenizer import Tokenizer
import numpy as np
import math
from collections import Counter
from tokenizer import Tokenizer
import pymongo
from pymongo import MongoClient
import operator
import json

class Query:
    """
    This class is responsible for queries inverted index and returns results
    """

    def __init__(self):
        # will use database information
        self.myclient = MongoClient("mongodb://localhost:27017/")
        # db = myclient['CS121_norm_100']
        self.db = self.myclient['CS121DB']


    def initializeQuery(self):
        """
        Is the main interface to run the query retrieval
        User must type QUIT to end the program
        """
        while True:
            print("Enter QUIT to exit")
            query = input("Enter a query: ")
            query = query.lower()
            if query == "QUIT":
                break
            else:
                # Tokenizes the query
                tokenObj = Tokenizer()
                query_list = tokenObj.tokenize(query)
                # Gets query vector
                query_vector = self.getWordNormal(query_list)
                # Gets top docids
                docIDS = self.getTopDoc(query_list)
                # Gets doc vector
                doc_normalized = self.getDocNormal(query_list, docIDS)
                # Compute cosine similarity and sorts in desending order
                sorted_doc_id_list = self.getCosineSim(query_vector, doc_normalized, query_list, docIDS)
                # Displays top 20 results
                print("Here are your results: \n")
                print(self.get_top20_url(sorted_doc_id_list))
        
        print("\n==================")
        print("Terminating program")
        print("==================\n")
        

    def getTop50Tag(self, query_list, docid_list):
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
                cursor = self.db[word[0]].aggregate([
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
            temp_list.append(tuple_item[0])
        
        return temp_list


    def getTopDoc(self, query_list):
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
            cursor = self.db[word[0]].aggregate([
            {"$match": {"_id": word}}, # matches with the id = word
            {"$unwind": "$doc_info"}, # it extracts the array ! gets the whole array
            {"$project":{
                "doc": "$doc_info.originalID",
                "tagScore": "$doc_info.tagScore",
                "norm": "$doc_info.normalized"
            }},
            {"$sort": { "tagScore": pymongo.DESCENDING}}, 
            {"$limit" : 700 }
            ])

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
        docID_list = self.getTop50Tag(query_list, docID_list)

        return docID_list


    def getDocNormal(self, query_list, docIDs):
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

        doc_vector = {}

        for word in query_list:
            vector_list = []
            counter = 0

            while counter < 20 and counter < len(docIDs):
                # we look for a matching case

                # getting norm
                cursor = self.db[word[0]].aggregate([
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
            doc_vector[word] = vector_list # each word we return norm vector 
        
        return doc_vector

    
    def getWordNormal(self, query_list):
        """
        Retrieve docID's normalize from mongoDB
        Parameter: 
            query_list
        """
        query_wt = []
        tfraw_dict = Counter(query_list)
        n = 37497 
        
        for word in query_list:
            tfwt = 1 + math.log10(tfraw_dict[word])
            
            cursor = self.db[word[0]].aggregate([
            {"$match": {"_id": word}}, # matches with the id = word
            {"$project":{
                "total": "$total"
            }}])

            cursor_list = list(cursor)

            if (len(cursor_list) == 1): # if we found a match
                # df = cursor_list[0]['total']
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



    def getCosineSim(self, query_vec, doc_normalized, query_list, doclist):
        """
        Retrieve docID's normalize from mongoDB
        Parameter: 
            query_vec, doc_normalized, query_list, doclist
        """
        # for word in query_normalized:
        doc_vect = []

        # following the query order 
        for word in query_list:
            doc_vect += [doc_normalized[word]]

        query_vec = np.array(query_vec)
        doc_vect = np.array(doc_vect)
        doc_vect = doc_vect.T
        
        doc_cossim = {}
        
        idx = 0
        for doc_row in doc_vect:
            doc_cossim[doclist[idx]] = (np.dot(query_vec, doc_row))
            idx += 1

        doc_cossim = sorted(doc_cossim.items(), key=operator.itemgetter(1),reverse=True)
        

        sorted_doc_id_list = []
        for tuple_item in doc_cossim:
            sorted_doc_id_list.append(tuple_item[0])
        
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


    def get_result_falsk(self, user_input):
        """
        For flask to display results
        Parameter: 
            user_input
        Return: url_list
        """
        tokenObj = Tokenizer()
        query_list = tokenObj.tokenize(user_input)
        query_vector = self.getWordNormal(query_list)
        docIDS = self.getTopDoc(query_list)
        doc_normalized = self.getDocNormal(query_list, docIDS)
        sorted_doc_id_list = self.getCosineSim(query_vector, doc_normalized, query_list, docIDS)
        url_list = self.get_top20_url(sorted_doc_id_list)

        return url_list
