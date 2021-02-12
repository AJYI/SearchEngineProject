from textblob import Word
from textblob import TextBlob
from bs4 import BeautifulSoup
from collections import Counter

class Tokenizer:
    """
    This class is responsible for building inverted index
    """

    def __init__(self):
        self.stopSet = set(line.strip() for line in open('stopWords.txt'))
        pass

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
                    processed_list.append(self.tokenizeWordWithBadCharacters(word))

                else:
                    """
                    The "good condition":
                        This is where anything without nonascii or non alpha num stuff will be appended to the processed_list
                        Keep in mind, it's expected that strings like
                        2009 will be cleared
                        regular words will be cleared
                        incorrect words like xtafasf could be cleared
                    """
                    # Lemmatizing the word
                    lem_word = self.lemmatize_with_post_tags(word)

                    # If lem_word is found in the removeStopWords function, then we pass
                    if self.removeStopWord(lem_word):
                        continue

                    # The good case, when all following conditions have been met
                    else:
                        processed_list.append(lem_word)

            except:
                # If an exception occurs, we will just go to the next iteration
                continue

        return processed_list
    

    def tokenizeWordWithBadCharacters(self, word):
        """
        A helper function of tokenize
        :param word = a word with bad characters that need to be processed
        :return: after the word with bad characters have been processed, it will a list
        """
        processed_text = ''
        word = word.lower()
        for i in range(len(word)):
            try:
                if not word[i].isalnum() or not word[i].isascii():
                    processed_text += ' '
                else:
                    processed_text += word[i]
            # If for some reason there is an error
            except:
                processed_text += ' '

        # We split the processed tokens and put it into a list
        pre_list = processed_text.split()
        for i in range(pre_list):
            lem_word = self.lemmatize_with_post_tags(pre_list[i])

            # If lem_word is found in the removeStopWords function, then we pass
            if self.removeStopWord(lem_word):
                pre_list(i).pop()
            
            pre_list[i] = lem_word
        return pre_list
        

    # A helper function for tokenize
    # This function properly lemmatizes with POS
    def lemmatize_with_post_tags(self, word):
        w = TextBlob(word)
        tag_dict = {"J": 'a', "N": 'n', "V": 'v', "R": 'r'}
        tag = tag_dict.get(w.tags[0][1][0], 'n')
        pre_lem = Word(word)
        lem_word = pre_lem.lemmatize(tag)
        return lem_word  


    def removeStopWord(self, word):
        """
        Helper function for tokenize
        :param word
        :return: True if the word is found in the stop word set / False if the word is not found in the stop word set
        """

        # We initailize self.stop_words so we don't create it over and over again :)
        if word in self.stopSet:
            return True
        else:
            return False


    def lemmatize(self, word):
        """
        Helper function for tokenize
        :param word
        :returns the lemmatized word
        """
        w = Word(word.lower())
        return w.lemmatize()


    # In the future there needs to be better functionalities here
    def htmlContentToList(self, url_data):
        """
        This function will get the url_data and split every word that is categorized as text in url_data
        :param url_data = the html text page string
        :returns a unprocessed list from url_data text
        """
        #unprocessed_list = list(url_data.find('p').getText().lower().split())
        unprocessed_list = list(url_data.getText(separator= ' ').lower().split())
        return unprocessed_list


    # def computeWordFrequencies(self, tokenized_list):
    #     """
    #     Purpose: counts the number of occurrences of each token in the token list (List<Token> tokens).
    #     Return: a sorted dictionary of counted words
    #     """
    #     count_dict = Counter(tokenized_list)
    #     dict_items = count_dict.items() # new
    #     sorted_dict = sorted(dict_items) # new
    #     return dict(sorted_dict)
    #     #return count_dict


    #An implementation idea of how the function will progress
    
    """
    Will be in order
    some arguement parameter for html file
    unprocessed_list = htmlContenetToList(url_data)
    tokenized_list = tokenize(unprocessed_list)
    frequency_dict = computeWordFrequencies(tokenized_list)

    In the end we will have a count_dict returned which will be used to add to the linked list that will be implemented soon
    """