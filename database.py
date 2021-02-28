import pymongo
from pathlib import Path
import os
from natsort import os_sorted
import math



class Database:


    def __init__(self):
        """
        The constructor
        User can change the db name in MongoDB to whatever they want, to do this, change self.db_name
        """
        self.cluster = pymongo.MongoClient()
        self.db_name = "CS121DBTester"
        self.db = self.cluster[self.db_name]


    def checkExistingDataBase(self):
        """
        Checks if the database exist,
        if True -> jumps right to the query part
        if False -> created the database that houses the inverted index
        """
        databases = pymongo.MongoClient()
        for i in databases.list_databases():
            if i['name'] == self.db_name:
                return True


    def write_to_database(self, docs):
        """
        This function writes to the database by using the the file inside the Cache/ directory.
        Param : docs is the total docs that the class index has gathered from iterating through the JSON File

        This function has two phases:
        (1) Creates the database from the Cache file(s) and only keeps track of the keys and the number of times(total) they are found within those cache files
        Reasoning for this is because we need that value BEFORE we calculate the tf-idf score
        (2) Reiterates through the Cache file to update the database. Since we didn't update anything but the key and total in the first phase, we now update the whole
        database with the relevant information. While doing this, we will calculate the tf-idf score

        Implications: Will essentially be O(2n) = O(n) and repeat of code
        """


        # This line of code is for when there are more than one files in the cache, we need it to be in numerical order
        # os_sorting for natsort
        # Source: https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort
        iterFiles = os_sorted(Path('Cache/').iterdir())

        # Phase 1
        print("\n==========================")
        print("Initializing the keys")
        print("==========================\n")
        for file in iterFiles:
            with file.open('r') as f:
                # Reading all the lines within the file
                for line in f:
                    """
                    Line data will be in the form of:
                    [KEY, UNIQUE_DOC_ID, DOC_ID, FREQUENCY, TF SCORE]
                    """

                    # This will convert the "Stringed" list into an actual list
                    db_list = eval(line)

                    # The first entry of the list is always the key
                    key = db_list[0]

                    # If the key starts with a numeric value then we put it into the num db
                    collection = self.db["Num"]
                    if key[0].isnumeric():
                        collection = self.db["Num"]

                    # If the key does not start with a numeric value(alphabets, then we put in into its corresponding char db)
                    else:
                        collection = self.db[key[0]]

                    """
                    Code will be commented out just incase we need for later.
                    """
                    # This checks whether the key exists in the database
                    # Source for this code
                    # https://stackoverflow.com/questions/25163658/mongodb-return-true-if-document-exists
                    if collection.count_documents({'_id': key}, limit=1) != 0:
                        collection.update({"_id": db_list[0]}, {"$inc": {"total": 1}})
                        continue
                    else:
                        # Inputs the key into the database if the key doesn't exist
                        post = {"_id": db_list[0], "total": 1, "doc_info": []}
                        collection.insert_one(post)
                        continue

        # Phase 2
        print("\n==========================")
        print("Writing to the database")
        print("==========================\n")
        for file in iterFiles:
            with file.open('r') as f:
                for line in f:
  
                    db_list = eval(line)

                    key = db_list[0]

                    collection = self.db["Num"]
                    if key[0].isnumeric():
                        collection = self.db["Num"]
                    else:
                        collection = self.db[key[0]]

                    """
                    This code will find the key id and will extract the total from the database entry
                    Then it will do the tfidf calculations and add the rest of the information into the database by updating the array entry
                    """
                    collDict = collection.find_one({"_id": key})
                    tot = collDict['total']
                    tfidf = db_list[3][5] * (1 + math.log10(docs/tot))

                    collection.update({"_id": db_list[0]}, {'$push': {
                        "doc_info": {"uniqueID": db_list[1], "originalID": db_list[2], "frequency": db_list[3][0], 'title': db_list[3][1], 'header': db_list[3][2], 'bold': db_list[3][3], 'body': db_list[3][4], 'tf-idf': tfidf}}})
                    continue


            # Will remove the file after it's content has been created within the database
            os.remove(file)