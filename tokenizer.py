from textblob import Word
from textblob import TextBlob, blob
from bs4 import BeautifulSoup
from collections import Counter
from pattern.en import lemma
import nltk


class Tokenizer:
    """
    This class is responsible for building inverted index
    """

    def __init__(self):
        self.stopSet = set(line.strip() for line in open('stopWords.txt'))


    def tokenize(self, sentence):
        """
        :param sentence
        :return: a tokenized list
        """
        # Tokenizes out the punctuations/underscore/and the other stuff
        fullTokenizedList = []
        try:
            processedSentence = ""
            if not sentence.isalnum() or not sentence.isascii():
                for i in range(len(sentence)):
                    try:
                        if not sentence[i].isalnum() or not sentence[i].isascii():
                            processedSentence += " "
                        else:
                            processedSentence += sentence[i]
                    except:
                        processedSentence += " "

            lemmaSentence = self.lemmatize(processedSentence)
            blob = TextBlob(lemmaSentence)
            tokenizedList = list(blob.words)
            
            # Checks for stop words, if stop words exists, it is removed
            for i in tokenizedList:
                if self.checkStopWord(i):
                    continue
                else:
                    fullTokenizedList.append(i)
        except Exception as e:
            # Used to check if there are errors that needs to be fixed
            print(e)
            print("here")
        return fullTokenizedList

    def lemmatize(self, sentence):
        word = sentence.split()
        newWordList = []
        for i in word:
            w = TextBlob(i)
            tag_dict = {"J": 'a', "N": 'n', "V": 'v', "R": 'r'}
            tag = tag_dict.get(w.tags[0][1][0], 'n')
            pre_lem = Word(i)
            lem_word = pre_lem.lemmatize(tag)
            newWordList.append(lem_word)
        return ' '.join(newWordList)


    def checkStopWord(self, word):
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


    # In the future there needs to be better functionalities here
    # inputt : url_data = soup
    def htmlContentSeparator(self, url_data):
        """
        This function will get the url_data and split every word that is categorized as text in url_data
        :param url_data = the html text page string
        :returns a unprocessed list from url_data text
        """
        return url_data.getText(separator= ' ').lower()

    # process list according to tags
    def soupTagImportance(self, soup):
        title = soup.find('title')
        tags_dict = {}
        title_unprocessed = self.htmlContentSeparator(title)

        title_tokenized_list = self.tokenize(title_unprocessed)

        tags_dict["title"] = title_tokenized_list
        title.extract()

        header_tokenized_list = []
        # remove heading 1,2,3
        h1 = soup.find('h1')
        if h1 is not None:
            h1_unprocessed_list = self.htmlContentSeparator(h1)
            header_tokenized_list = self.tokenize(h1_unprocessed_list)
            h1.extract()
            
            h2 = soup.find('h2')

            if h2 is not None:
                h2_unprocessed_list = self.htmlContentSeparator(h2)
                h2_tokenized = self.tokenize(h2_unprocessed_list)
                header_tokenized_list = header_tokenized_list + h2_tokenized
                h2.extract()

                h3 = soup.find('h3')

                if h3 is not None:
                    h3 = soup.find('h3')
                    h3_unprocessed_list = self.htmlContentSeparator(h3)
                    h3_tokenized = self.tokenize(h3_unprocessed_list)
                    header_tokenized_list = header_tokenized_list + h3_tokenized

                    h3.extract()
        tags_dict["header"] = header_tokenized_list
            
            
        bold_tokenized_list = []
        # remove bold
        bold = soup.find('b')
        if bold is not None:
            bold_unprocessed_list = self.htmlContentSeparator(bold)
            bold_tokenized_list = self.tokenize(bold_unprocessed_list)
            bold.extract()
        tags_dict["bold"] = bold_tokenized_list


        body_unprocessed_list = self.htmlContentSeparator(soup)
        body_tokenized_list = self.tokenize(body_unprocessed_list)

        tags_dict["body"] = body_tokenized_list  

        return tags_dict