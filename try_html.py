from tokenizer import Tokenizer
from bs4 import BeautifulSoup
import os
import lxml.html
import re


# 0/5 has only h1
# 0/6 has more than h1
htmlFile = os.path.join('WEBPAGES_RAW/', '0/10')
if os.path.isfile(htmlFile):
    with open(htmlFile) as fp:
        # soup contains HTML content
        soup = BeautifulSoup(fp, "lxml")
        print("0. HTML \n", soup.getText(separator= ' '))

        tokenObj = Tokenizer()
        # remove title
        title = soup.find('title')
        tags_dict = {}
        print("\n\n:: Removing title :\n")
        print("~~~Title soup type:", type(title))
        title_unprocessed_list = tokenObj.htmlContentToList(title)
        print("~~~title_unprocessed_list soup type:", type(title_unprocessed_list))
        print("title_unprocessed_list",title_unprocessed_list)
        title_tokenized_list = tokenObj.tokenize(title_unprocessed_list)
        print("\n1. title_tokenized_list\n", title_tokenized_list)
        
        tags_dict["title"] = title_tokenized_list
        
        title.extract()

        header_tokenized_list = []
        # remove heading 1,2,3
        h1 = soup.find('h1')
        if h1 is not None:
            print("\n\n:: Removing Headings :\n")
            print("...Removing", h1.name, "...")
            print(h1.text)
            h1_unprocessed_list = tokenObj.htmlContentToList(h1)
            print("~~~h1_unprocessed_list soup type:",h1_unprocessed_list)
            header_tokenized_list = tokenObj.tokenize(h1_unprocessed_list)
            print(header_tokenized_list)
            h1.extract()
            
            h2 = soup.find('h2')

            if h2 is not None:
                print("...Removing", h2.name, "...")
                # print(h2.text)
                h2_unprocessed_list = tokenObj.htmlContentToList(h2)
                h2_tokenized = tokenObj.tokenize(h2_unprocessed_list)
                print(h2_tokenized)
                header_tokenized_list = header_tokenized_list + h2_tokenized
                h2.extract()

                h3 = soup.find('h3')

                if h3 is not None:
                    h3 = soup.find('h3')
                    print("...Removing", h3.name, "...")
                    # print(h3.text)
                    h3_unprocessed_list = tokenObj.htmlContentToList(h3)
                    h3_tokenized = tokenObj.tokenize(h3_unprocessed_list)
                    print(h3_tokenized)
                    header_tokenized_list = header_tokenized_list + h3_tokenized

                    h3.extract()
        print("\n2. header_tokenized_list\n",header_tokenized_list)
        tags_dict["header"] = header_tokenized_list
            
            
        bold_tokenized_list = []
        # remove bold
        bold = soup.find('b')
        if bold is not None:
            print("\n\n:: Removing bold :\n")
            # print("... Removing ", bold.text, "...")
            bold_unprocessed_list = tokenObj.htmlContentToList(bold)
            bold_tokenized_list = tokenObj.tokenize(bold_unprocessed_list)
            bold.extract()
        print("\n3. bold_tokenized_list\n", bold_tokenized_list)
        tags_dict["bold"] = bold_tokenized_list

        print("\nLeft over ...")
        print("~~~Body soup type:", type(soup))
        body_unprocessed_list = tokenObj.htmlContentToList(soup)
        print("~~~body_unprocessed_list soup type:", type(title_unprocessed_list))
        print("~~~title_unprocessed_list soup type:", title_unprocessed_list)
        body_tokenized_list = tokenObj.tokenize(body_unprocessed_list)
        print("\n4. body_tokenized_list\n",body_tokenized_list)    

        tags_dict["body"] = body_tokenized_list    

        print("\n5. tags_dict\n")
        for key in tags_dict:
            print(key)
            print(tags_dict[key])
            print()


