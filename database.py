import pymongo
from pathlib import Path
import os


class Database:

    def __init__(self):
        self.cluster = pymongo.MongoClient()

        # Can customize database name here
        self.db_name = "CS121"
        self.db = self.cluster[self.db_name]

    def checkExistingDataBase(self):
        databases = pymongo.MongoClient()
        for i in databases.list_databases():
            if i['name'] == self.db_name:
                return True

    def write_to_database(self):
        print("\nWriting to database\n")
        iterFiles = Path('Cache/').iterdir()

        # Reading all the files in Cache
        for file in iterFiles:
            with file.open('r') as f:
                # Reading all the lines within the file
                for line in f:
                    # Expect a list data type
                    db_list = eval(line)
                    # The key that we will use to do our calculations
                    key = db_list[0]

                    # If the key starts with a numeric value then we put it into the num db
                    collection = self.db["Num"]
                    if key[0].isnumeric():
                        collection = self.db["Num"]
                    # If the key does not start with a numeric value(alphabets, then we put in into its corresponding char db)
                    else:
                        collection = self.db[key[0]]

                    # [KEY, UNIQUE_DOC_ID, DOC_ID, FREQUENCY]

                    # This checks whether the key exists in the database

                    # https://stackoverflow.com/questions/25163658/mongodb-return-true-if-document-exists
                    if collection.count_documents({'_id': key}, limit=1) != 0:
                        collection.update({"_id": db_list[0]}, {"$inc": {"total": 1}})
                        collection.update({"_id": db_list[0]}, {'$push': {
                            "doc_info": {"uniqueID": db_list[1], "OriginalID": db_list[2], "Frequency": db_list[3]}}})
                        continue
                    else:
                        # Inputs the key into the database if the key doesn't exist
                        post = {"_id": db_list[0], "total": 1, "doc_info": [
                            {"uniqueID": db_list[1], "OriginalID": db_list[2], "Frequency": db_list[3]}]}
                        collection.insert_one(post)
                        continue

            # Will remove the file after it's content has been created within the database
            os.remove(file)

