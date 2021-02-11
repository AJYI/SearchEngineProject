
# The attributes of the linked list
class LLAttribute:

    def __init__(self, docID, frequency):
        self.docID = docID
        self.frequency = frequency  # number of occurance in the token

    """
    Returns docID (string) of current token in the linked list
    """
    def getDocID(self):
        return self.docID

    """
    Return the frequency of the current token in this docID. 
    (NOT the frequency of the entire corpus)
    """
    def getFrequency(self):
        return self.frequency
