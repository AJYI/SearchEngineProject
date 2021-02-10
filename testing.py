import unittest
from index_constructor import Index

class TestStringMethods(unittest.TestCase):
    # Just the function itself without tokenizing
    def testLemmatize(self):
        index = Index()
        self.assertEquals(index.lemmatize("cars"), 'car')
        self.assertEquals(index.lemmatize("OcToPi"), 'octopus')
        self.assertEquals(index.lemmatize("informatics"), 'informatics')
        self.assertEquals(index.lemmatize("cars"), 'car')
        self.assertEquals(index.lemmatize("caresses"), 'caress')
        self.assertEquals(index.lemmatize("ponies"), 'pony')
        self.assertEquals(index.lemmatize("mass"), 'mass')
        self.assertEquals(index.lemmatize("gas"), 'gas')

    def testLemmatizeWithTokeinze(self):
        index = Index()
        tmp = ["cars'", "car's", "cars"]
        self.assertEquals(index.tokenize(tmp), ["car", "car", "car"])
    
    def testLemmatizeWithTokeinze2(self):
        index = Index()
        tmp = ["donkeys's"]
        self.assertEquals(index.tokenize(tmp), ["donkey"])

    def testLemmatizeWithStopWorks(self):
        index = Index()
        tmp = ["s", "the"]
        self.assertEquals(index.tokenize(tmp), [])

    def testComputeFreq1(self):
        index = Index()
        tmp = ["chicken" , "chicken" , "chicken", "chicken", "chicken"]
        self.assertEquals(index.computeWordFrequencies(tmp), {'chicken' : 5})       

    def testComputeFreq2(self):
        index = Index()
        tmp = ["nuggets" , "chicken" , "chicken", "chicken", "chicken"]
        self.assertEquals(index.computeWordFrequencies(tmp), {'chicken' : 4, 'nuggets' : 1 })

    def testComputeFreq3(self):
        index = Index()
        tmp = ["didnt" , "didn't" , "didn't", "didn't","didn't", "didnt'"]
        some_list = index.tokenize(tmp)
        self.assertEquals(index.computeWordFrequencies(some_list), {}) 

    def testComputeFreq4(self):
        index = Index()
        tmp = ["Alexs", "Alex's"]
        some_list = index.tokenize(tmp)
        self.assertEquals(index.computeWordFrequencies(some_list), {"Alex's" : 1})          
        
    def testComputeFreq5(self):
        index = Index()
        tmp = ["can't" , "cant" , "cant'"]
        some_list = index.tokenize(tmp)
        self.assertEquals(index.computeWordFrequencies(some_list), {"cant" : 2}) 

if __name__ == '__main__':
    unittest.main()