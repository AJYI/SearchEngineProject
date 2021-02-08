from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from bs4 import BeautifulSoup

class Index:
    """
    This class is responsible for building inverted index
    """

#    def __init__(self):

    def tokenize(self, unprocessed_list):
        """
        :param unprocessed_list: list of tokens that needs verification
        :return: a processed_list = A list of tokenized words
        """
        processed_list = []

        # Removed all the stop words within the unprocessed_list
        unprocessed_list = self.removeStopWords(unprocessed_list)

        for word in unprocessed_list:
            try:    




                pass
            except:
                # If an exception occurs, we will just go to the next iteration
                pass

        return processed_list


    def removeStopWords(self, word_list):
        """
        Helper function for tokenize
        :param word_list = a list of words that will be checked on for stop words
        :return: a new list of words that have stop words excluded
        """
        stop_words = set(stopwords.words('english'))

        no_stop_words_list = []

        # Iterates through all the words in the wordlist
        # Then checks if the word is in the stop list. 
        # If it is, do nothing
        # If not, then append to no_stop_word_list

        for word in word_list:
            if word in stop_words:
                pass
            no_stop_words_list.append(word)
        
        return no_stop_words_list


    def lemmatize(self, word):
        """
        Helper function for tokenize
        :param word
        :returns the lemmatized word
        """
        return WordNetLemmatizer().lemmatize(word)

    
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
