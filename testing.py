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
        
if __name__ == '__main__':
    unittest.main()