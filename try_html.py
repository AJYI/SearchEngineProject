from nltk.util import pr
from stanfordnlp.pipeline.core import Pipeline
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

## lemitize
def lemmatize(sentence):
    # now using spacy
    doc = spacy_nlp(sentence)
    return " ".join([token.lemma_ for token in doc])

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# 101 -> has weird capital I
# 138 -> raises error with Error in tokenize: list.remove(x): x not in list

url_smaple = "http://proquest.umi.com/cat/dog/pqdweb?index=4&did=000000111479923&SrchMode=1&sid=1&Fmt=3&VInst=PROD&VType=PQD&RQT=309&VName=PQD&TS=1078069852&clientId=1568"
url_sample2 = "https://stackoverflow.com/questions/7160737/hey-my-name-is-Faustina/how-to-validate-a-url-in-python-malformed-or-not"
url_smaple3 = "http://hpdma2.math.unipa.it/welcome.html"


if( (re.match(regex, url_smaple3) is not None) == True):

    total_list = []

    parse_url = urlparse(url_smaple3)
    netlock = parse_url[1]
    # add the netlock
    total_list.append(netlock)

    netlock_re = re.split('\W+', netlock)
    total_list = total_list + netlock_re

    # split the path
    path = parse_url[2]
    path_split = parse_url[2].split('/')

    for path in path_split:
        path = re.split('\W+', path)
        # total_list = total_list + path
        if path[0] != '':
            total_list = total_list + path

    print("total\n",total_list)

    



# htmlFile = os.path.join('WEBPAGES_RAW/', '0/138')
# if os.path.isfile(htmlFile):
#     with open(htmlFile) as fp:
#         # soup contains HTML content
#         soup = BeautifulSoup(fp, "lxml")

#         tokenObj = Tokenizer()
#         spimiObj = Spimi()
    

#         sentence = tokenObj.htmlContentSeparator(soup) # sentence -> string (alex's code)
#         sentence = tokenObj.tokenize(sentence) # tokenize -> returns list [string, string]

#         print(sentence)
        

        # word = "computing 2351"
        # print("Before")
        # print(word)
        # print("After")

        # tokenObj = Tokenizer()
        # print(tokenObj.lemmatize(word))
        # print(type(tokenObj.lemmatize(word)))
        

# print(lemmatize(word))

"""
import pymongo
# import pprint
# import json
# import warnings
from pymongo import MongoClient


### working getting information on DB 

def serach_in_db(db, text):
    frist_letter = text[0]
    return db[frist_letter].find_one()

myclient = MongoClient("mongodb://localhost:27017/")
db = myclient['CS121_20']

print("list of db", db.list_collection_names())

tokenObj = Tokenizer()

# enter = input("Enter to serach : ")
enter = "alice"
enter_list = tokenObj.tokenize(enter)
print("Entered list : ", enter_list)


# print(db.list_collection_names())
# print(serach_in_db)
# print(type(enter[0]))

# gets the first char and search the db
a  = enter[0]
print(serach_in_db(db,enter))

"""


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