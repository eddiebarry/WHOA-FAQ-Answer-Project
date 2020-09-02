import sys, os, lucene, json
sys.path.append('WHO-FAQ-Keyword-Engine')
sys.path.append('WHO-FAQ-Search-Engine')
sys.path.append('WHO-FAQ-Update-Engine')


from keyword_extractor import KeywordExtract
from search import SearchEngine
from query_generator import QueryGenerator
from index import IndexFiles
from org.apache.lucene.analysis.standard import StandardAnalyzer

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Index generator
Index = IndexFiles("./VaccineIndex.Index",StandardAnalyzer())
Index.indexFolder("./WHO-FAQ-Search-Engine/test_data/json_folder_data")
indexDir = Index.getIndexDir()

QueryGenTest = QueryGenerator(StandardAnalyzer())

# Keyword Extractor
jsonpath = "./WHO-FAQ-Keyword-Engine/test_excel_data/curated_keywords.json"
f = open(jsonpath,)
jsonObj = json.load(f)
keyword_extractor = KeywordExtract(jsonObj)

# Process query
query_string = "My child is sick with pneumonia She had been playing "+\
    "with her dog What will be the cost of vaccination"
    
boosting_tokens = keyword_extractor.parse_regex_query(query_string)
print(boosting_tokens)

# Create a lucene query
QueryGen = QueryGenerator(StandardAnalyzer(), use_synonyms=True)
query = QueryGen.build_query(query_string, \
    boosting_tokens, "OR_QUERY", field="Master Question")

print(query)

# Search Engine
SearchEngine = SearchEngine(indexDir, rerank=True)

hits = SearchEngine.search(query, \
        query_string=query_string, query_field="Master Question")
print("%s total matching documents." % len(hits))

for doc in hits:
    print("contents : " , doc[1], "\nscore : ", doc[0])