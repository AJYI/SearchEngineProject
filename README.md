Project 3 Search Engine:
Overall purpose of each python file:

Tokenizer:
Tokenizer is given an unprocessed_list (AKA all the text from html)
Then it returns a tokenized list that is lemmatized

spimi:
After the tokenizer has ran, it will go into the the Inverted_index.py and index everything alphabetically(By keys)
When memory threshold is > 80% it will write everything into a text file and it will be sorted.
The information that will be contained in the text file is in the form of:

                        [KEY, UNIQUE_DOC_ID, DOC_ID, FREQUENCY]

database:
We will be using mongoDB and it will need to be downloaded in order to have full functionality.
After the Inverted_index has been created, we will get the textfile(invertexIndexNo_x) and use it to create out database
Our database would be in the form of:

                        id: "key"
                        total: x
                        tf-idf: x
                        doc_info:Array
                            0 : Object
                                uniqueID: "x"
                                originalID: "x/x"
                                frequency: x
                            .
                            .
                            n