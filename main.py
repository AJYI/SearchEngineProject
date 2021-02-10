<<<<<<< HEAD
import atexit
import logging

import sys

from index_constructor import Index
from basic_query import Query
from bs4 import BeautifulSoup
from pathlib import Path
import os
if __name__ == "__main__":

    basepath = 'WEBPAGES_RAW\\'
    counter = 0
    endloop = False

    fileSize = len(os.listdir(basepath)) - 2  # number of folders in WEBPAGES_RAW

    for i in range(fileSize):
        basepath = 'WEBPAGES_RAW\\'
        folderPath = os.path.join(basepath, str(i))
        # print(folderPath)
        for fileName in os.listdir(folderPath):
            htmlFile = os.path.join(folderPath, fileName)
            # print(htmlFile)
            if os.path.isfile(htmlFile):
                with open(htmlFile) as fp:
                    try:
                        soup = BeautifulSoup(fp, "html.parser")
                        # if we have a broken HTML, then continue to next HTML file :)
                        if(bool(soup.find()) == False):
                            continue

                        # print(soup)
                        indexObj = Index()
                        unprocessed_list = indexObj.htmlContentToList(soup)
                        tokenized_list = indexObj.tokenize(unprocessed_list)
                        print(tokenized_list)
                        # frequency_dict = indexObj.computeWordFrequencies(tokenized_list)

                        # print(frequency_dict)

                        counter += 1
                        if (counter > 1):
                            break
                    except:
                        # We have a broken HTML. Go to the next HTML file!
=======
import atexit
import logging

import sys

from index_constructor import Index
from basic_query import Query
from bs4 import BeautifulSoup
from pathlib import Path
import os
if __name__ == "__main__":

    basepath = 'WEBPAGES_RAW\\'
    counter = 0
    endloop = False

    fileSize = len(os.listdir(basepath)) - 2  # number of folders in WEBPAGES_RAW

    for i in range(fileSize):
        basepath = 'WEBPAGES_RAW\\'
        folderPath = os.path.join(basepath, str(i))
        # print(folderPath)
        for fileName in os.listdir(folderPath):
            htmlFile = os.path.join(folderPath, fileName)
            # print(htmlFile)
            if os.path.isfile(htmlFile):
                with open(htmlFile) as fp:
                    try:
                        soup = BeautifulSoup(fp, "html.parser")
                        # if we have a broken HTML, then continue to next HTML file :)
                        if(bool(soup.find()) == False):
                            continue

                        # print(soup)
                        indexObj = Index()
                        unprocessed_list = indexObj.htmlContentToList(soup)
                        tokenized_list = indexObj.tokenize(unprocessed_list)
                        print(tokenized_list)
                        # frequency_dict = indexObj.computeWordFrequencies(tokenized_list)

                        # print(frequency_dict)

                        counter += 1
                        if (counter > 5):
                            break
                    except:
                        # We have a broken HTML. Go to the next HTML file!
>>>>>>> ff771bce1d5c40b271929df6370d3f27b77263ee
                        continue