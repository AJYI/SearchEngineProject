Project 3 Search Engine:
Overall purpose of each python file:

Tokenizer:
Tokenizer is given an unprocessed_list (AKA all the text from html)
Then it returns a tokenized list that is lemmatized

Inverted_index:
After the tokenizer has ran, it will go into the the Inverted_index.py and index everything alphabetically(By keys)
When memory threshold is > 80% it will write everything into a text file and it will be sorted.
The information that will be contained in the text file is in the form of:

    {KEY: NumberOfTimesSeenInLinkedList, [[DOC_ID?Frequency?MOREVARIABLESCANBEADDED], ....]}

    notice the: "DOC_ID.Frequency.MOREDATA.MOREDATA.MOREDATA". The reason why there are "." is because we can add as many information to it and later when it's added to the database
    it can be split up from the "." to get all the information without having to do so much work to extract the information
    Also, the the data that can be added in there is TF-IDF score and/or other ranking data.

Data_Base:
After the Inverted_index has been created, we will get the textfile created from all the key/value pair and add it to our database