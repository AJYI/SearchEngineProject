class LLAttribute:
    
    def __init__(self, uniqueDocID, docID, frequency):
        self.uniqueDocID = uniqueDocID
        self.docID = docID
        self.frequency = frequency  # number of occurance in the token


    """
    Returns the Unique docID (string) of current token in the linked list
    """
    def getUniqueDocID(self):
        return self.uniqueDocID


    """
    Returns docID (string) of current token in the linked list
    """
    def getDocID(self):
        return self.docID


    """
    Return the frequency of the current token in this docID. 
    (NOT the frequency of the entire corpus)
    """
    """
    Should return a list now
    """
    def getFrequency(self):
        return self.frequency
