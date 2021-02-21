import psutil
import os
from collections import OrderedDict
from collections import Counter
from llist import dllist
from LLAttribute import LLAttribute
import shutil
import gc


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
        self.invertedIndexName = "Cache/invertedIndexNo_"
        self.file = open(f"{self.invertedIndexName}{self.fileNO}.txt", 'w')
        self.docID = ""

        # Empty Dictionary
        self.word_dictionary = {}

        # Unique doc ID
        self.uniqueDocID = 0


    def create_block(self, token_stream, docID):
        """
        spimi_invert is similar to the psuedo code given in the lecture
        token_stream == The token that was tokenized by the tokenizer
        docID == The docID that the token_stream is from
        """

        # Gets the frequency dictionary from token_stream
        freq_of_word_dict = self.computeWordFrequencies(token_stream)

        # SPIMI memory check here
        # if memory(RAM) is past the 80% threshold then we write the block to disk(Essentially the while(free memory available))
        if float(psutil.virtual_memory().percent > 40):
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
                # self.file.write(f"\u007b'{i}':[{objLL.getUniqueDocID()}, {objLL.getDocID()}, {objLL.getFrequency()}]\u007d\n")
                self.file.write(
                    f"[\"{i}\", \"{objLL.getUniqueDocID()}\", \"{objLL.getDocID()}\", {objLL.getFrequency()}]\n")


    def conclude_spimi(self):
        """
        THIS FUNCTION NEEDS TO BE CALLED AFTER WE HAVE ITERATED THROUGH THE WHOLE CORPUS
        This function ensures that the last file is writen to the block and the file is now closed
        """
        self.order_dict()
        self.write_block_to_disk()
        self.free_memory()
        self.file.close()


    def computeWordFrequencies(self, token_stream):
        """
        Purpose: counts the number of occurrences of each token in the token list (List<Token> tokens).
        Return: a sorted dictionary of counted words
        """
        count_dict = Counter(token_stream)
        return count_dict


    def order_dict(self):
        """
        This is a helper function that will order the dictionary
        Currently there is not a place that this function will be effectively placed
        """
        self.word_dictionary = OrderedDict(sorted(self.word_dictionary.items()))