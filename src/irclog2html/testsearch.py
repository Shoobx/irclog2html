from pprint import pprint
from whoosh.index import open_dir
from whoosh.fields import Schema, TEXT, ID, NUMERIC, DATETIME
from whoosh.qparser import QueryParser

idx = open_dir("indexdir")

with idx.searcher() as searcher:
    query = QueryParser("line", idx.schema).parse("roadster")
    results = searcher.search(query)
    print results
    pprint(list(results))
