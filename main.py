from index_constructor import Index
from basic_query import Query
from bs4 import BeautifulSoup
import json
import os
if __name__ == "__main__":
    with open("WEBPAGES_RAW/bookkeeping.json") as keyFile:
        urlKey_dict = json.load(keyFile)
    basepath = 'WEBPAGES_RAW/'
    counter = 0
    for urlKey in urlKey_dict:
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

                    indexObj = Index()
                    unprocessed_list = indexObj.htmlContentToList(soup)
                    tokenized_list = indexObj.tokenize(unprocessed_list)
                    frequency_dict = indexObj.computeWordFrequencies(tokenized_list)
                    print(frequency_dict)

                    counter += 1
                    if (counter > 5):
                        break
                except:
                    # We have a broken HTML. Go to the next HTML file!
                    continue