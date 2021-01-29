import sys, os, json, requests, hashlib
import pysolr
import pdb

sys.path.append('WHO-FAQ-Search-Engine')

from solr_search import SolrSearchEngine
from rerank.ApiReranker import ApiReranker
from rerank.rerank_config import RE_RANK_ENDPOINT
from variation_generation.variation_generator import VariationGenerator
from synonym_expansion.synonym_expander import SynonymExpander

# Importing constants
from dotenv import load_dotenv
load_dotenv()

SearchEngineTest = SolrSearchEngine(
    rerank_endpoint=RE_RANK_ENDPOINT+"/api/v1/reranking",
    variation_generator_config=[
        VariationGenerator(
        path="./WHO-FAQ-Search-Engine/variation_generation/variation_generator_model_weights/model.ckpt-1004000",
        max_length=5),   #variation_generator
        # None,
        ["question"] #fields_to_expand
    ],
    synonym_config=[
        True, #use_wordnet
        True, #use_syblist
        "./WHO-FAQ-Search-Engine/synonym_expansion/syn_test.txt" #synlist path
    ],
    debug=True
)

'''
Create a collection + Add documents
'''
def test_collection_creation():
    SearchEngineTest.indexFolder("./accuracy_tests/intermediate_results/vla_data_formatted",
        project_id = "test",
        version_id = "test1"
    )

# test_collection_creation()

'''
Create a search query
'''
def test_query_generation():
    boosting_tokens = {
                        "type": ["agenda"],
                    }

    query_string = "Show me how to see my assignments"

    search_query, _ = SearchEngineTest.build_query(
            query_string, 
            boosting_tokens,
            "OR_QUERY",
            field="question"
        )

    temp='question:"Show" question:"me" question:"how" question:"to" question:"see" question:"my" question:"assignments"  OR type:"agenda"^1.05'
    
    assert search_query == temp, (" query is "+ search_query)
    return search_query

# test_query_generation()

'''
Search with query and confirm documents are present
'''
def test_search():
    search_query = test_query_generation()
    query_string = "Show me how to see my assignments"
    results = SearchEngineTest.search(
        query=search_query, 
        project_id="test", 
        version_id="test1",
        query_field="question*",
        query_string=query_string)
    
    exist = False
    for result in results:
        search_result = result[1].lower()

        this_exists = True
        for word in query_string.lower().split(" "):
            this_exists = this_exists and word in search_result

        exist = this_exists or exist

    assert exist, "query does not exist in search results"

# test_search()

'''
Delete collection
'''

def test_delete_collection():
    deletion_url = os.getenv("SOLR_ENDPOINT") + "/solr/admin/collections"
    x = requests.get(deletion_url,\
                {"action":"DELETE","name":"qa_test_test1"})

    assert x.status_code == 200

# test_delete_collection()/