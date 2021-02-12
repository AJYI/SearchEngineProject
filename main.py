from tokenizer import Tokenizer
from inverted_index import InvertedIndex
from basic_query import Query
from bs4 import BeautifulSoup
import json
import os
if __name__ == "__main__":
    with open("WEBPAGES_RAW/bookkeeping.json") as keyFile:
        urlKey_list = json.load(keyFile)
    basepath = 'WEBPAGES_RAW/'
    #counter = 0
    testSpimi = InvertedIndex()
    for urlKey in urlKey_list:
        # get HTML file's path
        htmlFile = os.path.join(basepath, urlKey)
        print(htmlFile)
        if os.path.isfile(htmlFile):
            with open(htmlFile) as fp:
                try:
                    soup = BeautifulSoup(fp, "html.parser")
                    # if we have a broken HTML, then continue to next HTML file
                    if not bool(soup.find()):
                        continue

                    tokenObj = Tokenizer()
                    unprocessed_list = tokenObj.htmlContentToList(soup)
                    tokenized_list = tokenObj.tokenize(unprocessed_list)
                    #frequency_dict = tokenObj.computeWordFrequencies(tokenized_list)
                    # print(frequency_dict)

                    testSpimi.spimi_invert(tokenized_list, urlKey)

                    # counter += 1
                    # if (counter > 200):
                    #     break
                except:
                    # We have a broken HTML. Go to the next HTML file!
                    continue
    testSpimi.write_block_to_disk()