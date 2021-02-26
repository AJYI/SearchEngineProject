from nltk.util import pr
from tokenizer import Tokenizer
from spimi import Spimi
from bs4 import BeautifulSoup
from collections import Counter
import os
import lxml.html
import re
import numpy as np


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