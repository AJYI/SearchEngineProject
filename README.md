# AAF's Search Engine:

AAF's Search Engine is written in python that allows the user to search in the webpages in UCI ICS domain. (http://www.ics.uci.edu)

## Installing
The requirements.txt file should list all Python libraries for the Search Engine. They will be installed using:
```
pip install -r requirements.txt
```

The requirements.txt includes 
```
pymongo
natsort
beautifulsoup4
lxml
numpy
psutil
```

## Overall purpose of each python file

### Tokenizer:
Tokenizer is given an unprocessed_list (AKA all the text from html)
Then it returns a tokenized list that is lemmatized

### spimi:
After the tokenizer has ran, it will go into the the Inverted_index.py and index everything alphabetically(By keys)
When memory threshold is > 80% it will write everything into a text file and it will be sorted.
The information that will be contained in the text file is in the form of:
```
[KEY, UNIQUE_DOC_ID, DOC_ID, FREQUENCY]
```

### database:
We will be using mongoDB and it will need to be downloaded in order to have full functionality.
After the Inverted_index has been created, we will get the textfile(invertexIndexNo_x) and use it to create out database
Our database would be in the form of:

```
id: "key"
total: int
idf: float
doc_info:Array
    0 : Object
        uniqueID: int
        originalID: string "x/x"
        frequency: int
        tagScore: int
        weight: float
        noormalized: float
    .
    .
    n
```

## Built With
* [mongoDB](https://www.mongodb.com/) - The database used

## Contributing
@AJYI
@fnyaung
@alicehj