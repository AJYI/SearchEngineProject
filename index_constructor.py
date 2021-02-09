from nltk.corpus import stopwords
from textblob import Word
from bs4 import BeautifulSoup
from collections import Counter

class Index:
    """
    This class is responsible for building inverted index
    """

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def tokenize(self, unprocessed_list):
        """
        :param unprocessed_list: list of tokens that needs verification
        :return: a processed_list = A list of tokenized words
        """
        processed_list = []

        for word in unprocessed_list:
            try:
                # When a word is not alphanum or is ascii
                if not word.isalnum() or not word.isascii():
                    # This function call will return a list
                    processed_list.extend(self.tokenizeWordWithBadCharacters(word))

                # Condition to lemmatize and remove stopwords
                else:
                    # Lemmatizing the word
                    lem_word = self.lemmatize(word)

                    # If lem_word is found in the removeStopWords function, then we pass
                    if self.removeStopWord(lem_word):
                        pass

                    # The good case, when all following conditions have been met
                    else:
                        processed_list.append(word)

            except:
                # If an exception occurs, we will just go to the next iteration
                pass

        return processed_list
    

    # Check for bugs incase
    def tokenizeWordWithBadCharacters(self, word):
        """
        A helper function of tokenize
        :param word = a word with bad characters that need to be processed
        :return: after the word with bad characters have been processed, it will a list
        """

        # From here we are going to check every character of the word to see if we can fix it up
        processed_text = ''

        for i in range(len(word)):
            try:
                if not word[i].isalnum() or not word[i].isascii():
                    processed_text += ' '
                else:
                    processed_text += word[i].lower()
            except:
                # If for some reason, an error occurs
                processed_text += ' '

        # After the if condtion, processed_text is completed and made
        # We now need to lemmatize and remove stop words
        processed_list = []

        for processed_word in processed_text.split():
            # Lemmatizing the word
            lem_word = self.lemmatize(processed_word) 

            # If lem_word is found in the removeStopWords function, then we pass
            if self.removeStopWord(lem_word):
                pass

            # The good case, when all following conditions have been met
            else:
                processed_list.append(processed_word)
        return processed_list


    def removeStopWord(self, word):
        """
        Helper function for tokenize
        :param word
        :return: True if the word is found in the stop word set / False if the word is not found in the stop word set
        """

        # We initailize self.stop_words so we don't create it over and over again
        if word in self.stop_words:
            return True
        else:
            return False


    def lemmatize(self, word):
        """
        Helper function for tokenize
        :param word
        :returns the lemmatized word
        """
        w = Word(word)
        w = w.singularize()
        return w.lemmatize()

    
    def htmlConvert(self, html_file):
        """
        This function will use beautiful soup, and convert html_file into url_data
        We only want this function to turn the html_file into a beautiful soup txt
        :param html_file = will be used to turn into html_code
        :returns html code
        """
        return BeautifulSoup(html_file, 'lxml')


    def htmlContentToList(self, url_data):
        """
        This function will get the url_data and split every word that is categorized as text in url_data
        :param url_data = the html text page string
        :returns a unprocessed list from url_data text
        """
        unprocessed_list = list(url_data.getText().lower().split())
        return unprocessed_list


    def computeWordFrequencies(self, tokenized_list):
        """
        Purpose: counts the number of occurrences of each token in the token list (List<Token> tokens).
        Return: a dictionary of counted words
        """
        count_dict = Counter(tokenized_list)
        return count_dict



    #An implementation idea of how the function will progress

    """
    Will be in order
    some arguement parameter for html file
    url_data = htmlConvert(some html File)
    unprocessed_list = htmlContenetToList(url_data)
    tokenized_list = tokenize(unprocessed_list)
    frequency_dict = computeWordFrequencies(tokenized_list)

    """