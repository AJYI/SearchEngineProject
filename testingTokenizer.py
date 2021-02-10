import unittest
from tokenizer import Tokenizer

class TestStringMethods(unittest.TestCase):
    # Just the function itself without tokenizing
    def testLemmatize(self):
        index = Tokenizer()
        self.assertEquals(index.lemmatize("cars"), 'car')
        self.assertEquals(index.lemmatize("OcToPi"), 'octopus')
        self.assertEquals(index.lemmatize("informatics"), 'informatics')
        self.assertEquals(index.lemmatize("cars"), 'car')
        self.assertEquals(index.lemmatize("caresses"), 'caress')
        self.assertEquals(index.lemmatize("ponies"), 'pony')
        self.assertEquals(index.lemmatize("mass"), 'mass')
        self.assertEquals(index.lemmatize("gas"), 'gas')

    def testLemmatizeWithTokeinze(self):
        index = Tokenizer()
        tmp = ["cars'", "car's", "cars"]
        self.assertEquals(index.tokenize(tmp), ["car", "car", "car"])
    
    def testLemmatizeWithTokeinze2(self):
        index = Tokenizer()
        tmp = ["donkeys's"]
        self.assertEquals(index.tokenize(tmp), ["donkey"])

    def testLemmatizeWithStopWorks(self):
        index = Tokenizer()
        tmp = ["s", "the"]
        self.assertEquals(index.tokenize(tmp), [])

    def testComputeFreq1(self):
        index = Tokenizer()
        tmp = ["chicken" , "chicken" , "chicken", "chicken", "chicken"]
        self.assertEquals(index.computeWordFrequencies(tmp), {'chicken' : 5})       

    def testComputeFreq2(self):
        index = Tokenizer()
        tmp = ["nuggets" , "chicken" , "chicken", "chicken", "chicken"]
        self.assertEquals(index.computeWordFrequencies(tmp), {'chicken' : 4, 'nuggets' : 1 })

    def testComputeFreq3(self):
        index = Tokenizer()
        tmp = ["didnt" , "didn't" , "didn't", "didn't","didn't", "didnt'"]
        some_list = index.tokenize(tmp)
        self.assertEquals(index.computeWordFrequencies(some_list), {}) 

    def testComputeFreq4(self):
        index = Tokenizer()
        tmp = ["Alexs", "Alex's"]
        some_list = index.tokenize(tmp)
        self.assertEquals(index.computeWordFrequencies(some_list), {"Alex's" : 1})          
        
    def testComputeFreq5(self):
        index = Tokenizer()
        tmp = ["can't" , "cant" , "cant'"]
        some_list = index.tokenize(tmp)
        self.assertEquals(index.computeWordFrequencies(some_list), {"cant" : 2}) 

if __name__ == '__main__':
    unittest.main()