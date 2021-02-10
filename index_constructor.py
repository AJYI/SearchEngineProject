from textblob import Word
from textblob import TextBlob
from bs4 import BeautifulSoup
from collections import Counter
import enchant

class Index:
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
        d = enchant.Dict("en_US")
        processed_list = []

        for word in unprocessed_list:
            try:
                # When a word is not alphanum or is ascii
                if not word.isalnum() or not word.isascii():
                    # This function call will return a list
                    returned_word = self.tokenizeWordWithBadCharacters(word)
                    if len(returned_word) == 0:
                        continue
                    processed_list.append(returned_word)

                # Condition to lemmatize and remove stopwords
                else:
                    # Checking whether the word is a word or not
                    if d.check(word) is False:
                        continue

                    # Lemmatizing the word
                    lem_word = self.lemmatize(word)

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
        s = list(word)

        # Checking is there is any bad characters within the beginning and the ends of the words
        if not s[0].isalnum() or not s[0].isascii():
            s.remove(s[0])
        if not s[-1].isalnum() or not s[-1].isascii():
            s.remove(s[-1])
        processed_word = "".join(s)

        """
        Will be using two flags
        If the first flag is true and second flag is false, we pass in the first flag word
        If the first flag is true and second flag is true, we pass in the second flag word
        If the first flag is false and second flag is false, return ""
        If the first flag is false and second flag is true, we pass in the second flag word
        """
        outer_flag1 = False
        outer_flag2 = False

        d = enchant.Dict("en_US")
        processed_text = ''

        if(d.check(processed_word)):
            outer_flag1 = True
        
        if self.removeStopWord(processed_word):
            return ""

        for i in range(len(processed_word)):
            try:
                if not processed_word[i].isalnum() or not processed_word[i].isascii():
                    processed_text += ''
                else:
                    processed_text += processed_word[i].lower()
            except:
                # If for some reason, an error occurs
                processed_text += ''
        
        # print(f"\n\n\n{processed_text}\n\n\n")
        # stemmer = PorterStemmer()

        lem_word = self.lemmatize(processed_text)
        # stem_word = stemmer.stem(processed_text)

        # print(f"\n\n\n{lem_word}\n\n\n")
        # print(f"\n\n\n{stem_word}\n\n\n")
        """
        if flag 1/2 is True/True, better to keep lem_word. Set outer_flag2 to true, and change processed_text = lem_word
        if flag 1/2 if True/false, better to keep lem_word. Set outer_flag2 to true, and change processed_text = lem_word
        if flag 1/2 is false/True, keep stem_word. Set outer_flag2 to true, and change processed_text = stem_word
        if flag 1/2 is false/false, set -> outer2_flag to false
        Then finally check if it is a stop word
        """
        inner_flag1 = False
        # inner_flag2 = False
        
        if d.check(lem_word):
            inner_flag1 = True
        # if d.check(stem_word):
        #     inner_flag2 = True

        if inner_flag1 is True:
            processed_text = lem_word
            outer_flag2 = True
        else:
            outer_flag2 = False
        # if inner_flag1 is True and inner_flag2 is True:
        #     processed_text = lem_word
        #     outer_flag2 = True
        # elif inner_flag1 is True and inner_flag2 is False:
        #     processed_text = lem_word
        #     outer_flag2 = True
        # elif inner_flag1 is False and inner_flag2 is True:
        #     processed_text = stem_word
        #     outer_flag2 = True
        # else:
        #     outer_flag2 = False
        
        # Checks whether the word we got is a stop word
        if self.removeStopWord(processed_text):
            outer_flag2 = False

        # print(f"text:{processed_text}| word:{processed_word}")

        # Final Check
        if outer_flag1 is True and outer_flag2 is True:
            return processed_text
        if outer_flag1 is True and outer_flag2 is False:
            return processed_word
        if outer_flag1 is False and outer_flag2 is True:
            return processed_text
        
        return ""

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

    
    # def htmlConvert(self, html_file):
    #     """
    #     This function will use beautiful soup, and convert html_file into url_data
    #     We only want this function to turn the html_file into a beautiful soup txt
    #     :param html_file = will be used to turn into html_code
    #     :returns html code
    #     """
    #     return BeautifulSoup(html_file, 'lxml')

    # In the future there needs to be better functionalities here
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
    unprocessed_list = htmlContenetToList(url_data)
    tokenized_list = tokenize(unprocessed_list)
    frequency_dict = computeWordFrequencies(tokenized_list)

    """