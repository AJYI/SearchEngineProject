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


    def tokenize(self, unprocessed_list):
        """
        :param unprocessed_list: list of tokens that needs verification
        :return: a processed_list = A list of tokenized words
        """
        processed_list = []

        for word in unprocessed_list:
            # try:
            # When a word is not alphanum or is ascii
            if not word.isalnum() or not word.isascii():
                # This function call will return a list
                processed_list.extend(self.tokenizeWordWithBadCharacters(word))

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

            # except:
            #     # If an exception occurs, we will just go to the next iteration
            #     continue

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
        pro_list = []
        for i in pre_list:
            lem_word = self.lemmatize_with_post_tags(i)

            # if i is stopWords , then we continue the loop
            if self.removeStopWord(lem_word):
                continue

            # If lem_word is found in the removeStopWords function, then we pass

            pro_list.append(lem_word)
        return pro_list


    # A helper function for tokenize
    # This function properly lemmatizes with POS
    def lemmatize_with_post_tags(self, word):
        w = TextBlob(word)
        tag_dict = {"J": 'a', "N": 'n', "V": 'v', "R": 'r'}
        tag = tag_dict.get(w.tags[0][1][0], 'n')
        pre_lem = Word(word)
        lem_word = pre_lem.lemmatize(tag)
        return lem_word  

        # just regular lemmatize
        # pre_lem = Word(word)
        # lem_word = pre_lem.lemmatize()
        # return lem_word  


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
    # inputt : url_data = soup
    def htmlContentToList(self, url_data):
        """
        This function will get the url_data and split every word that is categorized as text in url_data
        :param url_data = the html text page string
        :returns a unprocessed list from url_data text
        """
        #unprocessed_list = list(url_data.find('p').getText().lower().split())
        unprocessed_list = list(url_data.getText(separator= ' ').lower().split())
        return unprocessed_list

    # process list according to tags
    def soupTagImportance(self, soup):
        title = soup.find('title')
        tags_dict = {}
        title_unprocessed_list = self.htmlContentToList(title)
        title_tokenized_list = self.tokenize(title_unprocessed_list)
        
        tags_dict["title"] = title_tokenized_list
        
        title.extract()

        header_tokenized_list = []
        # remove heading 1,2,3
        h1 = soup.find('h1')
        if h1 is not None:
            h1_unprocessed_list = self.htmlContentToList(h1)
            header_tokenized_list = self.tokenize(h1_unprocessed_list)
            h1.extract()
            
            h2 = soup.find('h2')

            if h2 is not None:
                h2_unprocessed_list = self.htmlContentToList(h2)
                h2_tokenized = self.tokenize(h2_unprocessed_list)
                header_tokenized_list = header_tokenized_list + h2_tokenized
                h2.extract()

                h3 = soup.find('h3')

                if h3 is not None:
                    h3 = soup.find('h3')
                    h3_unprocessed_list = self.htmlContentToList(h3)
                    h3_tokenized = self.tokenize(h3_unprocessed_list)
                    header_tokenized_list = header_tokenized_list + h3_tokenized

                    h3.extract()
        tags_dict["header"] = header_tokenized_list
            
            
        bold_tokenized_list = []
        # remove bold
        bold = soup.find('b')
        if bold is not None:
            bold_unprocessed_list = self.htmlContentToList(bold)
            bold_tokenized_list = self.tokenize(bold_unprocessed_list)
            bold.extract()
        tags_dict["bold"] = bold_tokenized_list


        body_unprocessed_list = self.htmlContentToList(soup)
        body_tokenized_list = self.tokenize(body_unprocessed_list)

        tags_dict["body"] = body_tokenized_list    

        return tags_dict