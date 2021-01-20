import time
from locust import HttpUser, TaskSet, task, between, events


import sys, os, json, requests, hashlib, re
import pdb


inp = [
    {'query': 'can my daughter get immunised if she has a cold ?', 'user_id': '-1', 'trigger_search': True},
    {'query': 'booster', 'user_id': '768930bf736e05cc1c5609a91d9a7bff33493011c2576b7696a4ff4b676b079968d369178ea55c52c9c2f23ff87ed10ba0923c5fb63583d76aa605d826c2306b'},
    {'query': 'rubella', 'user_id': '768930bf736e05cc1c5609a91d9a7bff33493011c2576b7696a4ff4b676b079968d369178ea55c52c9c2f23ff87ed10ba0923c5fb63583d76aa605d826c2306b'},
    {'query': 'She is 6 years old', 'user_id': '768930bf736e05cc1c5609a91d9a7bff33493011c2576b7696a4ff4b676b079968d369178ea55c52c9c2f23ff87ed10ba0923c5fb63583d76aa605d826c2306b'}
]

def gentr_fn(alist):
    while 1:
        for j in alist:
            yield j
            
inp_gen = gentr_fn(inp)

class SearchEngineUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def index(self):
        # host = http://orchestrator-route-project-interakt-staging.apps.prod.lxp.academy.who.int
        past_id = '-1'
        x = inp_gen.__next__()
        if x['user_id'] == '-1':
            # pdb.set_trace()
            resp = self.client.get('/api/v2/qna', data=json.dumps(x)).json()
            past_id = resp['user_id']
        else:
            x['user_id']=past_id
            resp = self.client.get('/api/v2/qna', data=json.dumps(x)).json()