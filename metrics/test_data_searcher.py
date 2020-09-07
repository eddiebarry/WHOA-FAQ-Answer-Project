import sys, os, lucene, json
import hashlib
import pandas as pd

sys.path.append('../WHO-FAQ-Keyword-Engine')
sys.path.append('../WHO-FAQ-Search-Engine')
sys.path.append('../WHO-FAQ-Update-Engine')
sys.path.append('../WHO-FAQ-Dialog-Manager')

from org.apache.lucene.analysis.standard import StandardAnalyzer

from keyword_extractor import KeywordExtract
from search import SearchEngine
from query_generator import QueryGenerator
from index import IndexFiles

# Go thrugh the csv and query the search and 
# generate for each question asked, the corresponding list of scores
# returned

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print( 'lucene', lucene.VERSION)


    index_path = "./intermediate_results/VariationIndex.Index"
    index = IndexFiles(index_path,StandardAnalyzer())

    query_gen = QueryGenerator(StandardAnalyzer())
    
    indexDir = index.getIndexDir()
    search_engine = SearchEngine(indexDir, rerank=False)

    extractor_json_path = \
        "../WHO-FAQ-Keyword-Engine/test_excel_data/curated_keywords.json"
    f = open(extractor_json_path,)
    jsonObj = json.load(f)
    keyword_extractor= KeywordExtract(jsonObj)

    qa_list_path = "./intermediate_results/qa_user_list.csv"
    df = pd.read_csv(qa_list_path)

    accuracy = 0
    total = 0
    for idx, x in df.iterrows():
        try:
            query_string = x['User Question'].\
                replace("?","").replace("(","").replace(")","")

            boosting_tokens = keyword_extractor.parse_regex_query(query_string)
            query = query_gen.build_query(query_string, \
                    boosting_tokens, "OR_QUERY", field="Master_Question",\
                    boost_val=2.0)

            hits = search_engine.search(query, \
                    query_string=query_string, \
                    query_field="Master_Question", top_n=10)
            
            print(query_string)
            for doc in hits:
                if x['Master Question']==doc[1]:
                    accuracy +=1
                print(doc[1])
            print("*"*80)
            
            total += 1

        except Exception as e:
                print( "Failure in search", e)
    
    print(accuracy, total)
            



    # query_string = "What is the cost of pneumonia vaccine \?"
    
    # boosting_tokens = keyword_extractor.parse_regex_query(query_string)

    # query = query_gen.build_query(query_string, \
    #         boosting_tokens, "OR_QUERY", field="Master_Question",\
    #         boost_val=2.0)

    # hits = search_engine.search(query, \
    #         query_string=query_string, \
    #         query_field="Master_Question", top_n=10)

    # for doc in hits:
    #     print("Master Question", doc[1], "score", doc[0])