import psutil
from collections import OrderedDict
from collections import Counter
from llist import dllist, dllistnode
from LLAttribute import LLAttribute


# We will be creating a spimi index
class InvertedIndex():


    def __init__(self):
        # Have to create a new output_file
        self.fileNO = 0 # Starting at file number 0
        self.invertedIndexName = "Cache/invertedIndexNo_"
        self.word_dictionary = {}
        self.file = open(f"{self.invertedIndexName}{self.fileNO}.txt", 'w')
        self.docID = ""


    def spimi_invert(self, token_stream, docID):
        # Gets the frequencies of the whole document
        self.docID = docID
        freq_of_word_dict = self.computeWordFrequencies(token_stream)
        # Going to do a memory check here
        # if memory(RAM) is past the 85% threshold then we write the block to disk(Essentially the while(free memory available))
        if float(psutil.virtual_memory().percent > 85):
            self.write_block_to_disk()
            self.initializeNewFile()
            self.word_dictionary.clear() # We have freed up the memory here

        # This is line 4-10 from the SPIMI Pseudocode (NEED TO INCORPORATE THE freq_of_word)
        for i in freq_of_word_dict:
            if i not in self.word_dictionary:
                # Passing in key and value
                self.addNewTermToDictionary(i, LLAttribute(self.docID, freq_of_word_dict[i])) 
            else:
                # Passing in key and value
                self.addToExistingValueInDict(i, LLAttribute(self.docID, freq_of_word_dict[i]))
        
        # self.printDictionary()


    # AddToDictionary(dictionary, term(token))
    def addNewTermToDictionary(self, key, value):
        # self.word_dictionary = {} is the dictionary that you will work with
        # self.docID is the docID corresponding to the key/value
        # Key is the word(token)
        # Value is the frequency of that word(token)
        # You can add anything to make your function work
        newLL = dllist()
        newLL.append(value)
        self.word_dictionary[key] = newLL


    # addings to the existing value in the dict
    def addToExistingValueInDict(self, key, value):
        self.word_dictionary[key].append(value)

    
    # writing the file to disk
    def write_block_to_disk(self):
        for i in self.word_dictionary:
            self.file.write(f"{i}: ")
            for objLL in self.word_dictionary[i]:
                self.file.write(f"[{objLL.getDocID()},{objLL.getFrequency()}] ")
            self.file.write("\n")

    # initializes a new file
    def initializeNewFile(self):
        self.file.close()
        self.fileNO += 1
        self.file = open(f"{self.invertedIndexName}{self.fileNO}.txt")
    

    # When the program finishes running, must close the file
    def closeFinalFile(self):
        self.file.close()


    # Computing the frequencies of the word
    def computeWordFrequencies(self, token_stream):
        """
        Purpose: counts the number of occurrences of each token in the token list (List<Token> tokens).
        Return: a sorted dictionary of counted words
        """
        count_dict = Counter(token_stream)
        return count_dict

    def printDictionary(self):
        for key in self.word_dictionary:
            print(f"<{key}:", end='')
            for objLL in self.word_dictionary[key]:
                print(f"({objLL.getDocID()},{objLL.getFrequency()})", end="")
            print(">")