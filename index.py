from tokenizer import Tokenizer
from spimi import Spimi
from database import Database
from bs4 import BeautifulSoup
import lxml.html
import json
import os


class Index:
    def create_index(self):
        with open("WEBPAGES_RAW/bookkeeping.json") as keyFile:
            urlKey_list = json.load(keyFile)
        basepath = 'WEBPAGES_RAW/'

        # FOR DEBUGGING PURPOSES
        # counter = 0

        # Creating spimi object
        spimi = Spimi()
        # Creating database object
        mongoDataBase = Database()

        # This checks whether the database already exists or not
        # If it exists, there is no need to recreate a database
        if mongoDataBase.checkExistingDataBase() is True:
            print("Error: Database already exists")
            return

        # If database doesn't exist, then we create a new index(AKA invertedIndex)
        print("Initialization of creating the index")

        for urlKey in urlKey_list:
            # get HTML file's path
            htmlFile = os.path.join(basepath, urlKey)
            print(htmlFile)
            if os.path.isfile(htmlFile):
                with open(htmlFile, 'rb') as fp:
                    try:
                        soup = BeautifulSoup(fp, "lxml")
                        soupStr = str(soup).encode()
                        # if we have a broken HTML, then continue to next HTML file
                        if lxml.html.fromstring(soupStr).find('.//*') is None:
                            continue

                        tokenObj = Tokenizer()
                        unprocessed_list = tokenObj.htmlContentToList(soup)
                        tokenized_list = tokenObj.tokenize(unprocessed_list)
                        # frequency_dict = tokenObj.computeWordFrequencies(tokenized_list)
                        # print(frequency_dict)

                        spimi.create_block(tokenized_list, urlKey)

                        # FOR DEBUGGING PURPOSES
                        # counter += 1
                        # if (counter > 100):
                        #     break
                    except:
                        # We have a broken HTML. Go to the next HTML file!
                        print(f"EXCEPTED")
                        continue

        # Would need to write block to disk then clear
        spimi.conclude_spimi()

        # We write to the database
        mongoDataBase.write_to_database()