import time
from locust import HttpUser, TaskSet, task, between, events

import sys, os, json, requests, hashlib, re
import pdb


class SearchEngineUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def index(self):
        # new_url = index_url + '/anserini'
        # host = http://solr-cloud-project-interakt-staging.apps.prod.lxp.academy.who.int/solr/qa_testrm3_load_test
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