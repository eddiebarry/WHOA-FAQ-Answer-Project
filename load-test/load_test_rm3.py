import time
from locust import HttpUser, TaskSet, task, between, events


import sys, os, json, requests, hashlib, re
import pysolr
import pdb

sys.path.append('WHO-FAQ-Search-Engine')

from solr_search import SolrSearchEngine
from rerank.rerank_config import RE_RANK_ENDPOINT
from variation_generation.variation_generator import VariationGenerator

# Importing constants
from dotenv import load_dotenv
load_dotenv()


class SearchEngineUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def index(self):
        # new_url = index_url + '/anserini'
        # host = http://solr-cloud-project-interakt-staging.apps.prod.lxp.academy.who.int/solr/qa_testrm3_test1
        query = 'Do I need to pay for the hepatitis B vaccine'
        response = self.client.get('/anserini',data={"q":query})
        data = response.json()
        docs = data['docs']['docs']
        
        for idx, x in enumerate(docs):
            for key in x:
                x[key] = [x[key]]
            x['id']=str(idx)
        search_results_list = [x for x in docs]
        candidate = search_results_list[0]['question'][0].lower()
        for x in query.lower().split():
            assert x in candidate

    @events.test_start.add_listener
    def on_test_start(**kwargs):
        SearchEngineTest = SolrSearchEngine(
            rerank_endpoint=RE_RANK_ENDPOINT+"/api/v1/reranking",
            variation_generator_config=[
                VariationGenerator(\
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
            debug=True,
            use_rm3=True
        )
        SearchEngineTest.indexFolder("./accuracy_tests/intermediate_results/vsn_data_formatted",
            project_id = "testrm3",
            version_id = "test1"
        )
        print("index created")

    @events.test_stop.add_listener
    def on_test_stop(**kwargs):
        deletion_url = os.getenv("SOLR_ENDPOINT") + "/solr/admin/collections"
        x = requests.get(deletion_url,
                    {"action":"DELETE","name":"qa_testrm3_test1"})

        assert x.status_code == 200 or x.status_code == 504

        deletion_url = os.getenv("SOLR_ENDPOINT") + "/solr/admin/configs"
        x = requests.get(deletion_url,
                    {"action":"DELETE","name":"qa_testrm3_test1"})

        print(x.status_code)
        assert x.status_code == 200 or x.status_code == 400
        print("index deleted")