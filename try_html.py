from nltk.util import pr
from tokenizer import Tokenizer
from spimi import Spimi
from bs4 import BeautifulSoup
from collections import Counter
import os
import lxml.html
import re
import numpy as np
from urllib.parse import urlparse
import spacy	
spacy_nlp = spacy.load('en_core_web_sm')
import numpy as np
import math

# ## lemitize
# def lemmatize(sentence):
#     # now using spacy
#     doc = spacy_nlp(sentence)
#     return " ".join([token.lemma_ for token in doc])

import pymongo
# import pprint
# import json
# import warnings
from pymongo import MongoClient
from bson.objectid import ObjectId

tokenObj = Tokenizer()
### working getting information on DB 

"""
1) extract token#1's ALL uniqueID (3 & 9 & 48)
2) extract token#2 ALL uniqueID  (3 & 9 )
3) & the two lists from (1) & (2)  i get both list (1) &(2)
4) use the uniqueID from (3) to retrieve the tf-idf for both token #1 and token #2 (im adding tfidf in eadh document)

# computer & science = ? check sum tfidf.
# this is tfidf score for query  

"""

myclient = MongoClient("mongodb://localhost:27017/")
db = myclient['CS121_1000']

def search_in_db(db, text):
    # return dictionay 
    db_dict = {}
    # text first char in token
    first_letter = text[0]
    
    # this is text[0]
    alpha_db = db[first_letter]
    doc_info = alpha_db.find_one({"_id":text})['doc_info']

    # query length square root of total tfidf
    query_len = 0
    tf_idf = 0
    # query_vector = []

    # getting all the doc info
    print("for loop in doc info")
    for doc in doc_info:
        # db_dict[doc['uniqueID']] = doc['tf']*doc['idf']
        
        # query_len += float((doc['tf']*doc['idf'])**2)
        # # query_vector.append(doc['tf']*doc['idf'])
        # # print("query_vector: ", query_vector)

        # # query_len = np.power((doc['tf']*doc['idf']),2)
        db_dict[doc['uniqueID']] = doc['tf-idf']
        print(doc['uniqueID'], doc['tf-idf'])
    query_len = math.sqrt(query_len)
    print("query_len :", query_len)
    # query_vector = np.true_divide(query_vector, query_len)
    # print("query_vector :", query_vector)

    for key in db_dict:
        db_dict[key] = db_dict[key]/query_len

    return db_dict


# takes two dictionray and returns tfidf_query
def query_tfidf_add(db_dict_1, db_dict_2):
    # print(db_dict_1.keys())
    # print(db_dict_2.keys())
    list_keys = set(db_dict_1.keys()) & set(db_dict_2.keys())

    tfidf_query = {}

    if (len(db_dict_1) < len(db_dict_2)):
        for key in list_keys:
            tfidf_query[key] = db_dict_1[key] + db_dict_2[key]
    else:
        for key in list_keys:
            tfidf_query[key] = db_dict_2[key] + db_dict_1[key]

    return tfidf_query

# for loop part
# takes in - userinput : user input
def combine_query(db, userinput):
    # this will tokenize  + lemma
    input_list = tokenObj.tokenize(userinput)
    # input_list = userinput.split(' ')
    print(input_list)
    size = len(input_list)  # how many words in query

    if size == 1:
        return search_in_db(db, input_list[0])
    else:  # more than one words
        # oldDoc contains the array associated with the token (word)
        oldDoc = search_in_db(db, input_list[0])
        
        # print(input_list[0], "\n\n" ,oldDoc)
        for i in range(1, size):
            
            newDoc = search_in_db(db, input_list[i])
            # print(input_list[i], "\n\n", newDoc)
            oldDoc = query_tfidf_add(oldDoc, newDoc)

        return oldDoc


# tokenObj = Tokenizer()

enter1 = "cut" # frequency
enter2 = "career"
enter3 = "completeanns"

doc_normalized_dict = search_in_db(db, enter1)
print("\n\ntfidf query")
for key in doc_normalized_dict:
    print(key, doc_normalized_dict[key])
query_vector = doc_normalized_dict.values()
print("query_vector: ", list(query_vector))



"""
enter = input("Enter to search : ")

## 1. Represent the query as a weighted tf-idf vector.
tfidf_query = combine_query(db, enter)

print("\n\ntfidf query")
for key in tfidf_query:
    print(key, tfidf_query[key])


## 2. Represent each document as a weighted tf-idf vector
# <tfidf, tfidf, tfidf, tfidf>
tfidf_vector = np.array(tfidf_query.values() )
print(tfidf_vector)
"""

## 3. Compute the cosine similarity score for the query vector. and each document vector.


# print("\n\n")
# for key in tfidf_query:
#     print(key, tfidf_query[key])
# allkey = set().union(*alldict)



# # print(db['a'].find(myquery))
# a_db = db['a']
# one_a = db['a'].find_one()
# # objInstance = ObjectId('acm')
# id = "acm"

# # print(a_db.find_one({"_id":"acm"})['doc_info'])

# doc_info = a_db.find_one({"_id":"acm"})['doc_info']

# # how to get unique id 
# for doc in doc_info:
#     print(doc['uniqueID'], doc['tf-idf'] )

 


# print(a_db.find_one())
# print(a_db.find_one()['_id'])

# print(one_a['_id']) ## gives the  _id



# print("\ndatabase b:")
# print(db['b'].find_one())


# print(db.list_collection_names())
# print(serach_in_db)
# print(type(enter[0]))

# gets the first char and search the db
# a  = enter[0]
# print(search_in_db(db,enter))



# regex = re.compile(
#         r'^(?:http|ftp)s?://' # http:// or https://
#         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
#         r'localhost|' #localhost...
#         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
#         r'(?::\d+)?' # optional port
#         r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# # 101 -> has weird capital I
# # 138 -> raises error with Error in tokenize: list.remove(x): x not in list

# url_smaple = "http://proquest.umi.com/cat/dog/pqdweb?index=4&did=000000111479923&SrchMode=1&sid=1&Fmt=3&VInst=PROD&VType=PQD&RQT=309&VName=PQD&TS=1078069852&clientId=1568"
# url_sample2 = "https://stackoverflow.com/questions/7160737/hey-my-name-is-Faustina/how-to-validate-a-url-in-python-malformed-or-not"
# url_smaple3 = "http://hpdma2.math.unipa.it/welcome.html"


# if( (re.match(regex, url_smaple3) is not None) == True):

#     total_list = []

#     parse_url = urlparse(url_smaple3)
#     netlock = parse_url[1]
#     # add the netlock
#     total_list.append(netlock)

#     netlock_re = re.split('\W+', netlock)
#     total_list = total_list + netlock_re

#     # split the path
#     path = parse_url[2]
#     path_split = parse_url[2].split('/')

#     for path in path_split:
#         path = re.split('\W+', path)
#         # total_list = total_list + path
#         if path[0] != '':
#             total_list = total_list + path

#     print("total\n",total_list)

    



# htmlFile = os.path.join('WEBPAGES_RAW/', '0/236')
# if os.path.isfile(htmlFile):
#     with open(htmlFile) as fp:
#         # soup contains HTML content
#         soup = BeautifulSoup(fp, "lxml")

#         tokenObj = Tokenizer()
#         spimiObj = Spimi()
    

#         sentence = tokenObj.htmlContentSeparator(soup) # sentence -> string (alex's code)
#         print("\n\n~~ B4 tokenize sentence ~~\n")
#         print(sentence)

#         sentence = tokenObj.tokenize(sentence) # tokenize -> returns list [string, string]
#         print("\n\n~~ sentence ~~\n")
#         print(sentence)
        


############ !!!!! lemmatize function problem when i do 0/236, it doesnt work
# not all the words are lematizing correctlly 

# word = """the webdav working group met two times at the washington ietf meeting,
# on monday and tuesday, december 8-9, 1997, and 78 people attended one
# or both of the sessions. the chair was jim whitehead, and notes were
# recorded by alec dun, del jensen, and rohit khare, then edited by jim
# whitehead"""
# # print("Before")
# # print(word)
# print("~~~~~After")
# print(lemmatize(word))

# tokenObj = Tokenizer()
# print(tokenObj.lemmatize(word))
# print()

# print("tokenizer")
# print(tokenObj.tokenize(word))
# # print(type(tokenObj.lemmatize(word)))
        

# print(lemmatize(word))




"""
# 0/5 has only h1
# 0/6 has more than h1
htmlFile = os.path.join('WEBPAGES_RAW/', '0/6')
if os.path.isfile(htmlFile):
    with open(htmlFile) as fp:
        # soup contains HTML content
        soup = BeautifulSoup(fp, "lxml")

        tokenObj = Tokenizer()
        spimiObj = Spimi()
        

        # get the frequency of the word occurance 
        unprocessed_list = tokenObj.htmlContentToList(soup)
        tokenized_list = tokenObj.tokenize(unprocessed_list)
        # print(tokenized_list)
        word_freq_dict = Counter(tokenized_list)
        # print(count_word_freq)

        # get the total length 
        total_words = len(tokenized_list)

        # normalize TF for document
        for word in word_freq_dict:
            word_freq_dict[word] = word_freq_dict[word] / total_words
        
        print(word_freq_dict)

        # try to get the IDF for the each term
#         getIDF(total_no_document, no_doc_with_term)

#         print()

def getIDF(total_no_document, no_doc_with_term):
    idf = 1 + np.log(total_no_document/no_doc_with_term)
"""