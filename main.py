from index import Index
from basic_query import Query

if __name__ == "__main__":
    # Component 1 - Index / Component 3 - pre-ranking
    createIndex = Index()
    createIndex.create_index()

    # Component 2 - Search and Retrieve
    query = Query()
    query.initializeQuery()

