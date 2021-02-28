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

        # Total Approved Documented
        docs = 0

        # FOR DEBUGGING PURPOSES
        counter = 0

        #############################################################################
        # PHASE 1: We create the text file that will have the data for inverted index
        #############################################################################


        # Creating spimi object and database object
        spimi = Spimi()
        mongoDataBase = Database()

        # This checks whether the database already exists or not
        # If it exists, there is no need to recreate a database
        if mongoDataBase.checkExistingDataBase() is True:
            print("Initializing the query")
            return

        print("Initialization of creating the index")

        for urlKey in urlKey_list:

            # FOR DEBUGGING PURPOSES
            if (counter >= 20):
                break
            counter += 1

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

                        # New implementation for Alice function
                        tokenized_dict = tokenObj.soupTagImportance(soup)
                        #print(tokenized_dict)

                        # new implemntation
                        spimi.create_block(tokenized_dict, urlKey)

                        docs +=1

                    except Exception as e:
                        # Used to check if there are errors that needs to be fixed
                        print(f"Problem in createIndex: {e}")
                        continue

        # After the loop has finished, we must conclude the spimi to make sure all information is written to disk
        spimi.conclude_spimi()

        ################################################################
        # PHASE 2: We write to the database/Creating the inverted index
        ################################################################
        
        mongoDataBase.write_to_database(docs)