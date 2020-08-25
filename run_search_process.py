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
Index.indexFolder("./WHO-FAQ-Keyword-Engine/test_excel_data/json_data")
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
QueryGen = QueryGenerator(StandardAnalyzer())
query = QueryGen.build_query(query_string, \
    boosting_tokens, "OR_QUERY", field="Master Question")

print(query)

# Search Engine
SearchEngine = SearchEngine(indexDir)

hits = SearchEngine.search(query, top_n=10)
search_docs  = hits.scoreDocs
print("%s total matching documents." % len(search_docs))

for scoreDoc in search_docs:
    doc = SearchEngine.return_doc(scoreDoc.doc)
    print("question : " , doc.get("Master Question"),\
        "\nAnswer : " , doc.get("Master Answer"), \
        "\nscore : ", scoreDoc.score)