# import sys, os, lucene, json
# sys.path.append('WHO-FAQ-Keyword-Engine')
# sys.path.append('WHO-FAQ-Search-Engine')
# sys.path.append('WHO-FAQ-Update-Engine')


# from keyword_extractor import KeywordExtract
# from search import SearchEngine
# from query_generator import QueryGenerator
# from index import IndexFiles
# from org.apache.lucene.analysis.standard import StandardAnalyzer

# from rerank.rerank_config import RE_RANK_ENDPOINT

# lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# # Index generator
# Index = IndexFiles("./VaccineIndex.Index",StandardAnalyzer())
# Index.indexFolder(\
#     "./accuracy_tests/intermediate_results/vsn_data_variations")

# indexDir = Index.getIndexDir()

# QueryGenTest = QueryGenerator(StandardAnalyzer())

# # Keyword Extractor
# jsonpath = "./accuracy_tests/unique_keywords.json"
# f = open(jsonpath,)
# jsonObj = json.load(f)
# keyword_extractor = KeywordExtract(jsonObj)

# # Process query
# query_string = "What should i do about cumpolsory vaccinations if i have allergies"
    
# boosting_tokens = keyword_extractor.parse_regex_query(query_string)
# print(boosting_tokens)

# # Create a lucene query
# QueryGen = QueryGenerator(StandardAnalyzer(), \
#         synonym_config=[
#             False, #use_wordnet
#             False, #use_syblist
#             "./WHO-FAQ-Search-Engine/synonym_expansion/synlist.txt" #synlist path
#         ])
# query = QueryGen.build_query(query_string, \
#     boosting_tokens, "OR_QUERY", field="question")

# print(query)

# # Search Engine
# SearchEngine = SearchEngine(
#     indexDir, 
#     rerank_endpoint=RE_RANK_ENDPOINT
# )

# hits = SearchEngine.search(query, \
#         query_string=query_string, query_field="question")
# print("%s total matching documents." % len(hits))

# for doc in hits:
#     print("contents : " , doc[1], "\nscore : ", doc[0])

'''
Create a collection
'''

'''
Add documents
'''

'''
Create a search query
'''

'''
Search with query and confirm documents are present
'''

'''
Delete collection
'''