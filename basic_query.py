from tokenizer import Tokenizer

class Query:
    """
    This class is responsible for queries inverted index and returns results
    """

    def __init__(self):
        # will use database information
        pass


    def initializeQuery(self):
        """
        Is the main interface to run the query retrieval
        User must type QUIT to end the program
        """
        while True:
            query = input("Enter a query: ")
            query = query.lower()
            if query == "QUIT":
                break
            else:
                # Add some function that tokenizes the query
                tokenizedQuery = self.tokenize(query)
                resultsList = self.getDatabaseResults(tokenizedQuery)
                print("Here are your results: \n")
                self.printResults(resultsList)
        
        print("\n==================")
        print("Terminating program")
        print("==================\n")

    def tokenize(self, query):
        """
        Function tokenizes the query
        Returns a list that contains the tokenized query
        """
        tokenObj = Tokenizer()
        tokenized_query = tokenObj.tokenize(query)
        return tokenized_query
    

    def getDatabaseResults(self, tokenizedQuery):
        """
        Uses the database to get the links
        This function will return a list of links that are according the the tf-idf score, cosine similarity, and html tags
        """
        #Write your functionality here
        return tokenizedQuery


    def printResults(self, resultsList):
        """
        Essentially a toString function to print out the resultsList
        The resultsList is a list of all the links that will be printed
        """
        print(resultsList)
        # number = 0
        # for i in resultsList:
        #     print(f"{number}: {i}")
        #     number+=1
        # pass
