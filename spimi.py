import psutil
import os
from collections import OrderedDict
from collections import Counter
from llist import dllist
from LLAttribute import LLAttribute
import shutil
import gc
import math


# We will be creating a spimi index
class Spimi:

    def __init__(self):
        # Making/Remaking the Cache dir everytime this function constructor has ran
        try:
            os.makedirs("Cache")
        except:
            shutil.rmtree("Cache", ignore_errors=True)
            os.makedirs("Cache")

        # Initializing the first page we will go through
        self.fileNO = 0  # Starting at file number 0
        self.invertedIndexName = "Cache/"
        self.file = open(f"{self.invertedIndexName}{self.fileNO}.txt", 'w')
        self.docID = ""

        # Empty Dictionary
        self.word_dictionary = {}

        # Unique doc ID
        self.uniqueDocID = 0


    def create_block(self, token_dict, docID):
        """
        spimi_invert is similar to the psuedo code given in the lecture
        token_stream == The token that was tokenized by the tokenizer
        docID == The docID that the token_stream is from
        """

        # Gets the frequency dictionary from token_stream
        freq_of_word_dict = self.computeWordFrequencies(token_dict)

        # SPIMI memory check here
        # if memory(RAM) is past the 80% threshold then we write the block to disk(Essentially the while(free memory available))
        if float(psutil.virtual_memory().percent > 70):
            # Will order the dictionary
            self.order_dict()

            # Will create a block that will contain the sorted dictionary with all the relevant information
            self.write_block_to_disk()

            # Clearing up the potentially HUGE dictionary
            self.free_memory()

            self.initializeNewFile()

        # This is line 4-10 from the SPIMI Pseudocode
        """
        IN THE FUTURE WE CAN ADD SOME FUNCTIONALITY FOR TF-IDF or RANKING stuff as a parameter to addNewTerm
        """
        for i in freq_of_word_dict:
            if i not in self.word_dictionary:
                # Passing in a new key and adding the data to it
                self.addNewTermToDictionary(i, LLAttribute(self.uniqueDocID, docID, freq_of_word_dict[i]))
            else:
                # Finding the existing key and adding the relevant data to it
                self.addToExistingValueInDict(i, LLAttribute(self.uniqueDocID, docID, freq_of_word_dict[i]))

        self.uniqueDocID += 1


    def addNewTermToDictionary(self, key, value):
        """
        Is a helper function of spimi_invert.
        This function will add a new term to the dictionary
        Key == docID
        value = freq_of_word_dict[i]
        """
        newLL = dllist()
        newLL.append(value)
        self.word_dictionary[key] = newLL


    def addToExistingValueInDict(self, key, value):
        """
        Is a helper function for spimi_invert.
        This function will add an existing linkedList value to to the key
        Key == docID
        value = freq_of_word_dict[i]
        """
        self.word_dictionary[key].append(value)


    def free_memory(self):
        """
        Is a helper function for spimi_invert
        This function will free memory when memory threshold is high
        """
        self.word_dictionary.clear()
        gc.collect()


    def initializeNewFile(self):
        """
        Is a helper function for spimi_invert
        After the function write_block_to_disk() or free_memory() or BOTH has ran
        We will close the old file and initialize a new file(new block)
        """
        self.file.close()
        self.fileNO += 1
        self.file = open(f"{self.invertedIndexName}{self.fileNO}.txt", 'w')


    def write_block_to_disk(self):
        """
        Is a helper function for spimi_invert
        Will write the dictionary to the disk. File is under Cache and is named invertedIndexNo_x.txt
        FILE WILL BE WRITTEN AS
        [KEY, UNIQUE_DOC_ID, DOC_ID, FREQUENCY]
        """
        for i in self.word_dictionary:
            for objLL in self.word_dictionary[i]:
                self.file.write(
                    f"[\"{i}\", {objLL.getUniqueDocID()}, \"{objLL.getDocID()}\", {objLL.getFrequency()}]\n")


    def conclude_spimi(self):
        """
        THIS FUNCTION NEEDS TO BE CALLED AFTER WE HAVE ITERATED THROUGH THE WHOLE CORPUS
        This function ensures that the last file is writen to the block and the file is now closed
        """
        self.order_dict()
        self.write_block_to_disk()
        self.free_memory()
        self.file.close()

    def order_dict(self):
        """
        This is a helper function that will order the dictionary
        Currently there is not a place that this function will be effectively placed
        """
        self.word_dictionary = OrderedDict(sorted(self.word_dictionary.items()))


    # Need to better functionalize this
    def computeWordFrequencies(self, token_dict):
        """
        We will use the token dict that that contains will data in the form of
        ['title':[], 'header':[], 'bold':[], 'body':[]]
        then we will create a dictionary for each of the keys and use it to create the 
        new dict (count_dict)

        count_dict will be in the form of:
        ['someKey': [total(titleTotal + headerTotal + boldTotal + bodyTotal), titleTotal, headerTotal, boldTotal, BodyTotal, TF_Score]]

        Purpose: counts the number of occurrences of each token in the token list (List<Token> tokens).
        Return: a sorted dictionary of counted words, number of titles, number of headers, number of bolds, and number of body
        Essentially [Value_Total, title_total, header_total, bold_total, body_total]
        """
        count_dict_title = Counter(token_dict['title'])
        count_dict_header = Counter(token_dict['header'])
        count_dict_bold = Counter(token_dict['bold'])
        count_dict_body = Counter(token_dict['body'])
        
        # Initializing an empty dict
        count_dict = {}
        # Total words in the tokenized_dict
        #total_words = 0

        # for the count_dict_title, keys in this first entry will ALWAYS BE unique
        for i in count_dict_title:
            count_dict[i] = [count_dict_title[i], count_dict_title[i], 0, 0, 0, 0]
            #total_words += count_dict_title[i]
        
        # for header
        # for the count_dict_headers, keys might already exist
        for i in count_dict_header:
            # if the key exists in the dictionary
            if i in count_dict:
                count_dict[i][0] = count_dict[i][0] + count_dict_header[i]
                count_dict[i][2] = count_dict_header[i]
                #total_words += count_dict_header[i]
            # if it doesnt exist add it to the dictionary
            else:
                count_dict[i] = [count_dict_header[i], 0, count_dict_header[i], 0, 0, 0]
                #total_words += count_dict_header[i]
        
        # for bold
        # for the count_dict_bold, keys might already exist
        for i in count_dict_bold:
            # if the key exists in the dictionary
            if i in count_dict:
                count_dict[i][0] = count_dict[i][0] + count_dict_bold[i]
                count_dict[i][3] = count_dict_bold[i]
                #total_words += count_dict_bold[i]
            # if it doesnt exist add it to the dictionary
            else:
                count_dict[i] = [count_dict_header[i], 0, 0, count_dict_bold[i], 0, 0]
                #total_words += count_dict_bold[i]
        
        # for body
        # for the count_dict_body, keys might already exist
        for i in count_dict_body:
            # if the key exists in the dictionary
            if i in count_dict:
                count_dict[i][0] = count_dict[i][0] + count_dict_body[i]
                count_dict[i][4] = count_dict_body[i]
                #total_words += count_dict_body[i]
            # if it doesnt exist add it to the dictionary
            else:
                count_dict[i] = [count_dict_body[i], 0, 0, 0, count_dict_body[i], 0]
                #total_words += count_dict_body[i]
        
        # Calculates the TF-SCORE
        for i in count_dict:
            if count_dict[i][0] != 0:
                count_dict[i][5] = 1 + math.log10(count_dict[i][0])

        return count_dict

    # # Need to better functionalize this
    # def computeWordFrequencies(self, token_dict):
    #     """
    #     We will use the token dict that that contains will data in the form of
    #     ['title':[], 'header':[], 'bold':[], 'body':[]]
    #     then we will create a dictionary for each of the keys and use it to create the 
    #     new dict (count_dict)

    #     count_dict will be in the form of:
    #     ['someKey': [total(titleTotal + headerTotal + boldTotal + bodyTotal), titleTotal, headerTotal, boldTotal, BodyTotal, TF_Score]]

    #     Purpose: counts the number of occurrences of each token in the token list (List<Token> tokens).
    #     Return: a sorted dictionary of counted words, number of titles, number of headers, number of bolds, and number of body
    #     Essentially [Value_Total, title_total, header_total, bold_total, body_total]
    #     """
    #     count_dict_title = Counter(token_dict['title'])
    #     count_dict_header = Counter(token_dict['header'])
    #     count_dict_bold = Counter(token_dict['bold'])
    #     count_dict_body = Counter(token_dict['body'])
        
    #     # Initializing an empty dict
    #     count_dict = {}
    #     # Total words in the tokenized_dict
    #     #total_words = 0

    #     # for the count_dict_title, keys in this first entry will ALWAYS BE unique
    #     for i in count_dict_title:
    #         count_dict[i] = [count_dict_title[i], count_dict_title[i], 0, 0, 0, 0]
    #         #total_words += count_dict_title[i]
        
    #     # for header
    #     # for the count_dict_headers, keys might already exist
    #     for i in count_dict_header:
    #         # if the key exists in the dictionary
    #         if i in count_dict:
    #             count_dict[i][0] = count_dict[i][0] + count_dict_header[i]
    #             count_dict[i][2] = count_dict_header[i]
    #             #total_words += count_dict_header[i]
    #         # if it doesnt exist add it to the dictionary
    #         else:
    #             count_dict[i] = [count_dict_header[i], 0, count_dict_header[i], 0, 0, 0]
    #             #total_words += count_dict_header[i]
        
    #     # for bold
    #     # for the count_dict_bold, keys might already exist
    #     for i in count_dict_bold:
    #         # if the key exists in the dictionary
    #         if i in count_dict:
    #             count_dict[i][0] = count_dict[i][0] + count_dict_bold[i]
    #             count_dict[i][3] = count_dict_bold[i]
    #             #total_words += count_dict_bold[i]
    #         # if it doesnt exist add it to the dictionary
    #         else:
    #             count_dict[i] = [count_dict_header[i], 0, 0, count_dict_bold[i], 0, 0]
    #             #total_words += count_dict_bold[i]
        
    #     # for body
    #     # for the count_dict_body, keys might already exist
    #     for i in count_dict_body:
    #         # if the key exists in the dictionary
    #         if i in count_dict:
    #             count_dict[i][0] = count_dict[i][0] + count_dict_body[i]
    #             count_dict[i][4] = count_dict_body[i]
    #             #total_words += count_dict_body[i]
    #         # if it doesnt exist add it to the dictionary
    #         else:
    #             count_dict[i] = [count_dict_body[i], 0, 0, 0, count_dict_body[i], 0]
    #             #total_words += count_dict_body[i]
        
    #     # Calculates the TF-SCORE
    #     for i in count_dict:
    #         if count_dict[i] != 0:
    #             count_dict[i][5] = 1 + math.log10(count_dict[i][0])

    #     return count_dict

    