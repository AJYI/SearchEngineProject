from textblob import Word
from textblob import TextBlob, blob
from bs4 import BeautifulSoup
from collections import Counter
import pattern
from nltk.stem import WordNetLemmatizer
import re
import datetime


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
            lemmaSentence = self.lemmatize(sentence)
            lemmaList = lemmaSentence.split()
            lemmaListNoNum = self.checkForRawNumbers(lemmaList)
            lemmaListTokenized = self.tokenizeBadCharacters(lemmaListNoNum)
            lemmaSentence = " ".join(lemmaListTokenized)

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
            print(f"Error in tokenize: {e}")
        return fullTokenizedList
    

    def checkForRawNumbers(self, lemmaList):
        """
        This function will check if raw number exist within the html page
        We are doing this because we noticed that the numbers inflates our db size immensely
        This will filter out pages like 35/269
        """
        returnList = []
        for word in lemmaList:
            try:
                float(word)
                continue
            except:
                returnList.append(word)
        return returnList

    
    def tokenizeBadCharacters(self, lemmaListNoNum):
        """
        This function will tokenize bad characters
        bad characters = anything with comma, dashes, underscore, etc
        """
        filteredList = []
        for word in lemmaListNoNum:
            # Checks whether the word is a time
            if self.checkTimeWord(word) is True:
                filteredList.append(word)
                continue

            # Checks the dates01
            elif self.checkNumberedDates(word) is True:
                filteredList.append(word)
                continue

            # mainly when links are passed into the string
            elif not word.isalnum() or not word.isascii():
                processedWord = ""
                for i in range(len(word)):
                    try:
                        if not word[i].isalnum() or not word[i].isascii():
                            processedWord += " "
                        else:
                            processedWord += word[i]
                    except:
                        processedWord += " "
                filteredList.append(processedWord)
            else:
                filteredList.append(word)
        #print(f"tokenizedBad{filteredList}")
        return filteredList


    def checkTimeWord(self, word):
        # Source: https://stackoverflow.com/questions/1322464/python-time-format-check
        # This function checks whether the string word is in a format of a time
        time = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
        return bool(time.match(word))
         
    
    def checkNumberedDates(self, word):
        """
        https://www.tutorialspoint.com/python/time_strptime.htm
        https://stackoverflow.com/questions/23581128/how-to-format-date-string-via-multiple-formats-in-python
        This will check whether the string word is in the format of a date(numbers only) example 1/1/2020
        We will use multiple format
        # Trying different formats
        """
        
        for formats in ("%d-%b-%Y", "%m-%d-%Y", "%m-%d-%y", "%m/%d/%Y", "%m/%d/%y", "%m.%d.%y, %m.%d.%Y"):
            try:
                datetime.datetime.strptime(word,formats)
                return True
            except:
                pass
        return False


    # Returns a lemmatized sentence
    def lemmatize(self, sentence):
        # SOURCE: https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
        tmpSentence = TextBlob(sentence)
        return " ".join([w.lemmatize() for w in tmpSentence.words])


    def checkStopWord(self, word):
        """
        Helper function for tokenize
        :param word
        :return: True if the word is found in the stop word set / False if the word is not found in the stop word set
        """
        #print(word)

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
        sentence = ""
        try:
            sentence = url_data.getText(separator= ' ').lower()
        except Exception as e:
            print(f"ErrorInHTMLContent: {e}")
            return sentence
        return sentence


    # process list according to tags
    def soupTagImportance(self, soup):
        title = soup.find('title')
        tags_dict = {}

        # For the title
        if title is None:
            # From observation, if title doesn't exist, then it's most likely some type of doc file
            # For example observe doc 0/438 or 39/373
            tags_dict["title"] = []
            tags_dict["title"] = []
            tags_dict['header'] = []
            tags_dict['bold'] = []
            tags_dict['body'] = []
            return tags_dict
        else:
            title_unprocessed = self.htmlContentSeparator(title)

            title_tokenized_list = self.tokenize(title_unprocessed)

            tags_dict["title"] = title_tokenized_list
            title.extract()

        # For the h1, h2, h3
        header_tokenized_list = []
        # remove heading 1,2,3
        h1 = soup.find('h1')
        if h1 is not None:
            h1_unprocessed_list = self.htmlContentSeparator(h1)
            h1_tokenized_list = self.tokenize(h1_unprocessed_list)
            header_tokenized_list = h1_tokenized_list
            h1.extract()
            
        h2 = soup.find('h2')
        if h2 is not None:
            h2_unprocessed_list = self.htmlContentSeparator(h2)
            h2_tokenized_list = self.tokenize(h2_unprocessed_list)
            header_tokenized_list = header_tokenized_list + h2_tokenized_list
            h2.extract()

        h3 = soup.find('h3')
        if h3 is not None:
            h3_unprocessed_list = self.htmlContentSeparator(h3)
            h3_tokenized_list = self.tokenize(h3_unprocessed_list)
            header_tokenized_list = header_tokenized_list + h3_tokenized_list
            h3.extract()

        # create a new entry header in tag_dict    
        tags_dict["header"] = header_tokenized_list

        # remove bold
        bold = soup.find('b')
        if bold is not None:
            bold_unprocessed_list = self.htmlContentSeparator(bold)
            bold_tokenized_list = self.tokenize(bold_unprocessed_list)
            bold.extract()
            tags_dict["bold"] = bold_tokenized_list
        else:
            tags_dict["bold"] = []

        # For the body
        body_unprocessed = self.htmlContentSeparator(soup)
        if body_unprocessed is None:
            tags_dict["body"] = []
        else:
            body_tokenized_list = self.tokenize(body_unprocessed)

            tags_dict["body"] = body_tokenized_list  

        return tags_dict