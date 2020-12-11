import sys, os, json, requests, hashlib
import pysolr
import pdb
import pandas as pd

search_engine_path = "/usr/src/WHOA-FAQ-Answer-Project/WHO-FAQ-Search-Engine"
keyword_extractor_path = '/usr/src/WHOA-FAQ-Answer-Project/WHO-FAQ-Keyword-Engine'

sys.path.append(search_engine_path)
sys.path.append(keyword_extractor_path)

from solr_search import SolrSearchEngine
from rerank.ApiReranker import ApiReranker
from rerank.rerank_config import RE_RANK_ENDPOINT
from variation_generation.variation_generator import VariationGenerator
from synonym_expansion.synonym_expander import SynonymExpander
from keyword_extractor import KeywordExtract

# Importing constants
from dotenv import load_dotenv
load_dotenv()



# SearchEngineTest = SolrSearchEngine(
#     rerank_endpoint=RE_RANK_ENDPOINT+"/api/v1/reranking",
#     variation_generator_config=[
#         VariationGenerator(\
#         path= search_engine_path+ "/variation_generation/variation_generator_model_weights/model.ckpt-1004000",
#         max_length=5),   #variation_generator
#         # None,
#         ["question"] #fields_to_expand
#     ],
#     synonym_config=[
#         True, #use_wordnet
#         True, #use_syblist
#         search_engine_path+"/synonym_expansion/syn_test.txt" #synlist path
#     ],
#     debug=True
# )



# extractor_json_path = "/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/unique_keywords.json"

# f = open(extractor_json_path,)
# jsonObj = json.load(f)
# keyword_extractor= KeywordExtract(jsonObj)

# qa_list_path = "/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/intermediate_results/qa_user_list_1500.csv"
# df = pd.read_csv(qa_list_path)

# accuracy = 0
# total = 0

# rerank_test = []
# for idx, x in df.iterrows():
#     # try:
#     query_string = x['User Question'].\
#         replace("?","").replace("(","")\
#             .replace(")","").replace("-","").replace("\"","").replace("'","")
#     print(query_string)

#     boosting_tokens = keyword_extractor.parse_regex_query(query_string)
#     search_query, _ = SearchEngineTest.build_query(\
#             query_string, \
#             boosting_tokens,\
#             "OR_QUERY",
#             field="question"
#         )

#     top_n = 50
#     hits = SearchEngineTest.search(
#         query=search_query, 
#         project_id="test", 
#         version_id="test1",
#         query_field="question*",
#         query_string=query_string,
#         top_n = top_n)
    
#     rerank_test.append([query_string, x['Master Question'], hits])  

#     for doc in hits:
#         if x['Master Question']==doc[1].split(' ||| ')[0]:
#             accuracy +=1

#     total += 1

#     print("*"*80)

# print(accuracy, total, accuracy/total)

# '''
# Delete collection
# '''

# def test_delete_collection():
#     deletion_url = os.getenv("SOLR_ENDPOINT") + "/solr/admin/collections"
#     x = requests.get(deletion_url,\
#                 {"action":"DELETE","name":"qa_test_test1"})

#     assert x.status_code == 200

# # test_delete_collection()

class CalcMetrics:
    def __init__(self):
        self.SearchEngineTest = SolrSearchEngine(
            rerank_endpoint=RE_RANK_ENDPOINT+\
                "/api/v1/reranking",
            variation_generator_config=[
                VariationGenerator(\
                path= search_engine_path+ \
                    "/variation_generation"+\
                    "/variation_generator_model_weights/"+\
                    "model.ckpt-1004000",
                max_length=5),   #variation_generator
                # None,
                ["question"] #fields_to_expand
            ],
            synonym_config=[
                True, #use_wordnet
                True, #use_syblist
                search_engine_path+\
                    "/synonym_expansion/syn_test.txt" #synlist path
            ],
            debug=True
        )

        extractor_json_path = "/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/unique_keywords.json"

        f = open(extractor_json_path,)
        jsonObj = json.load(f)
        self.keyword_extractor= KeywordExtract(jsonObj)

        qa_list_path = "/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/intermediate_results/qa_user_list_1500.csv"
        self.df = pd.read_csv(qa_list_path)
    
    def get_accuracy(self, top_n=50):
        #Index all documents in a folder
        self.SearchEngineTest.indexFolder("/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/intermediate_results/vsn_data_variations",
            project_id = "test",
            version_id = "test1"
        )

        # Calculate accuracy
        accuracy = 0
        total = 0
        rerank_test = []

        for idx, x in self.df.iterrows():
            query_string = x['User Question'].\
                replace("?","").replace("(","")\
                    .replace(")","").replace("-","").replace("\"","").replace("'","")

            boosting_tokens = self.keyword_extractor.parse_regex_query(query_string)
            search_query, _ = self.SearchEngineTest.build_query(\
                    query_string, \
                    boosting_tokens,\
                    "OR_QUERY",
                    field="question"
                )

            hits = self.SearchEngineTest.search(
                query=search_query, 
                project_id="test", 
                version_id="test1",
                query_field="question*",
                query_string=query_string,
                top_n = top_n)
            
            rerank_test.append([query_string, x['Master Question'], hits])  

            for doc in hits:
                if x['Master Question']==doc[1].split(' ||| ')[0]:
                    accuracy +=1

            total += 1

        print("*"*80)
        print(accuracy, total, accuracy/total)

        assert total > 0

        # Delete collection
        deletion_url = os.getenv("SOLR_ENDPOINT") + "/solr/admin/collections"
        x = requests.get(deletion_url,\
                    {"action":"DELETE","name":"qa_test_test1"})

        assert x.status_code == 200

        return accuracy/ total

if __name__ == "__main__":

    metrics = CalcMetrics()
    print(metrics.get_accuracy())