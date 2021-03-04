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
<<<<<<< HEAD
        self.db_name = "CS121_norm_100"
=======
        self.db_name = "CS121Test"
>>>>>>> ef997798a6f764dd1512a4b5f002a5994ffac4e1
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
        (1) Uses the txt file in cache to get the total amount a key has been seen. Results would be put into total_dict. This will be necessary for the idf calculation.
        (2) Creates the database while looking through the total_dict to calculate the tf-idf score and insert the values associated with the keys.
        """


        # This line of code is for when there are more than one files in the cache, we need it to be in numerical order
        # os_sorting for natsort
        # Source: https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort
        iterFiles = os_sorted(Path('Cache/').iterdir())

        # Phase 1
        total_dict = {}

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

                    key = db_list[0]

                    # Checking if key is in dict
                    if key in total_dict:
                        total_dict[key] += 1
                    else:
                        total_dict[key] = 1

        # Phase 2
        # The keys for the nomalized_dict will be db_list[1]
        normalized_dict = {}

        print("\n==========================")
        print("Normalizing")
        print("==========================\n")
        for file in iterFiles:
            with file.open('r') as f:
                for line in f:

                    db_list = eval(line)

                    key = db_list[0]
                    uniqueID = db_list[1]

                    # We need these values to do normalization
                    tot = total_dict[key]
                    tf = db_list[3][5]
                    idf = math.log10(docs/tot)
                    weight = tf * idf

                    # Checking if key is in dict
                    if uniqueID in normalized_dict:
                        normalized_dict[uniqueID] += (weight * weight)
                    else:
                        normalized_dict[uniqueID] = weight * weight


        # Phase 3
        print("\n==========================")
        print("Writing to the database")
        print("==========================\n")
        for file in iterFiles:
            with file.open('r') as f:
                for line in f:
                    """
                    # db_list is in the format of:
                    db_list[0] = Key
                    db_list[1] = UniqueIdentifier
                    db_list[2] = docID(posting)
                    db_list[3][0] = total
                    db_list[3][1] = title
                    db_list[3][2] = header
                    db_list[3][3] = bold
                    db_list[3][4] = body
                    db_list[3][5] = tf score
                    """

                    db_list = eval(line)

                    key = db_list[0]
                    uniqueID = db_list[1]

                    collection = self.db["Num"]
                    if key[0].isnumeric():
                        collection = self.db["Num"]
                    else:
                        collection = self.db[key[0]]

                    """
                    This code will find the get the value associated to the key of total_dict
                    Then it will do the tfidf calculations and add the rest of the information into the database by updating the array entry
                    """
                    # is the class variable for the key and value pair of the txt file
                    tot = total_dict[key]
                    #tfidf = db_list[3][5] * (math.log10(docs/tot))
                    tf = db_list[3][5]
                    idf = (math.log10(docs/tot))
                    weight = tf * idf
                    length = math.sqrt(normalized_dict[uniqueID])
                    #print(f"{key}: {length}")


                    if collection.count_documents({'_id': key}, limit=1) != 0:
<<<<<<< HEAD
                        collection.update({"_id": db_list[0]}, {'$push': {
=======
                        collection.update({"_id": db_list[0]}, {'$push': { ''
>>>>>>> ef997798a6f764dd1512a4b5f002a5994ffac4e1
                        "doc_info": {"uniqueID": db_list[1], "originalID": db_list[2], "frequency": db_list[3][0], 'title': db_list[3][1], 'header': db_list[3][2], 'bold': db_list[3][3], 'body': db_list[3][4], 'weight': weight, 'normalized': (weight / length)}}})
                        continue
                    else:
                        # Inputs the key into the database if the key doesn't exist
<<<<<<< HEAD
                        post = {"_id": db_list[0], "total": total_dict[key], "doc_info": [{"uniqueID": db_list[1], "originalID": db_list[2], "frequency": db_list[3][0], 'title': db_list[3][1], 'header': db_list[3][2], 'bold': db_list[3][3], 'body': db_list[3][4], 'weight': weight, 'normalized': (weight / length)}]}
=======
                        post = {"_id": db_list[0], "total": total_dict[key], "idf": idf , "doc_info": [{"uniqueID": db_list[1], "originalID": db_list[2], "frequency": db_list[3][0], 'title': db_list[3][1], 'header': db_list[3][2], 'bold': db_list[3][3], 'body': db_list[3][4], 'weight': weight, 'normalized': (weight / length)}]}
>>>>>>> ef997798a6f764dd1512a4b5f002a5994ffac4e1
                        collection.insert_one(post)
                        continue


            # Will remove the file after it's content has been created within the database
            os.remove(file)