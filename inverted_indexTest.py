import unittest
from tokenizer import Tokenizer
from inverted_index import InvertedIndex
from bs4 import BeautifulSoup

class TestStringMethods(unittest.TestCase):
    # Just the function itself without tokenizing
    def testWriting(self):
        docID = "0/0"
        test = InvertedIndex()
        word_list = ["Dog", "Chicken"]
        test.spimi_invert(word_list, docID)

        docID = "1/11"
        word_list = ["Alex", "Faustina", "Dog", "Dog"]
        test.spimi_invert(word_list, docID)


        test.write_block_to_disk()
        test.closeFinalFile()


if __name__ == '__main__':
    unittest.main()