import requests ,hashlib, json, os, pickle, timeit, pdb, sys
from statistics import mean 
import pytest

from dotenv import load_dotenv
from data.helpers import populate_1500_questions
load_dotenv()

urls = [
    os.getenv("LOCAL_URL"),
    os.getenv("REMOTE_URL"),
]

"""
Batch Keyword Extract Test
"""
def test_batch_keyword_extract():
    batch_keyword_input = {
        "question_answer_list": [
            {
                "question": "My child is sick where can he get measles vaccine ?",
                "answer": "Please go to khandala",
                "id": "1"
            },
            {
                "question": "My child is sick where can he get rubella vaccine ?",
                "answer": "Please go to khandala",
                "id": "2"
            },
            {
                "question": "My child is sick where can he get polio vaccine ?",
                "answer": "Please go to khandala",
                "id": "3"
            }
        ]
    }
    batch_keyword_response ={
        "questions_keywords_list": [
            {
                "id": "1",
                "keywords": {
                    "disease_1": [
                        "measles"
                    ],
                    "disease_2": [
                        "measles"
                    ],
                    "other_conditions_or_symptoms_etc": [
                        "sick",
                        "child",
                        "baby"
                    ],
                    "subject_1_immunization": [
                        "vaccination",
                        "immunization"
                    ],
                    "subject_2_vaccination_general": [
                        "vaccination",
                        "travel"
                    ],
                    "subject_person": [
                        "baby",
                        "child",
                        "daughter",
                        "son"
                    ],
                    "vaccine_1": [
                        "measles"
                    ],
                    "vaccine_2": [
                        "measles"
                    ],
                    "who_is_writing_this": [
                        "child",
                        "son",
                        "daughter"
                    ]
                }
            },
            {
                "id": "2",
                "keywords": {
                    "disease_1": [
                        "rubella"
                    ],
                    "disease_2": [
                        "rubella"
                    ],
                    "other_conditions_or_symptoms_etc": [
                        "sick",
                        "child",
                        "baby"
                    ],
                    "subject_1_immunization": [
                        "vaccination",
                        "immunization"
                    ],
                    "subject_2_vaccination_general": [
                        "vaccination",
                        "travel"
                    ],
                    "subject_person": [
                        "baby",
                        "child",
                        "daughter",
                        "son"
                    ],
                    "vaccine_1": [
                        "rubella"
                    ],
                    "vaccine_2": [
                        "rubella"
                    ],
                    "who_is_writing_this": [
                        "child",
                        "son",
                        "daughter"
                    ]
                }
            },
            {
                "id": "3",
                "keywords": {
                    "other_conditions_or_symptoms_etc": [
                        "sick",
                        "child",
                        "baby"
                    ],
                    "subject_1_immunization": [
                        "vaccination",
                        "immunization"
                    ],
                    "subject_2_vaccination_general": [
                        "vaccination",
                        "travel"
                    ],
                    "subject_person": [
                        "baby",
                        "child",
                        "daughter",
                        "son"
                    ],
                    "vaccine_1": [
                        "polio"
                    ],
                    "vaccine_2": [
                        "polio"
                    ],
                    "who_is_writing_this": [
                        "child",
                        "son",
                        "daughter"
                    ]
                }
            }
        ]
    }
    for url in urls:
        base_url = url  + "/api/v2/batch_keyword_extract"
        r = requests.post(base_url,
            data=json.dumps(batch_keyword_input))
        data = r.json()
                
        assert data == batch_keyword_response, \
            "Keyword extract failed for " + url

"""
Batch QA index 
"""

def test_qa_indexing():
    qa_index_data = populate_1500_questions(\
        dir_ = "./accuracy_tests/intermediate_results/vsn_data_formatted")


    response_data = {
        "estimated_time": 4377,
        "project_id": "999",
        "status": "ok",
        "version_id": "0"
    }

    for url in urls:
        base_url = url  + "/api/v2/train_bot_json_array"
        r = requests.post(base_url,
            data=json.dumps(qa_index_data))
        data = r.json()
        # pdb.set_trace()
        assert data == response_data, \
            ("Test QA index failed for " + url)

"""
Bot host test
"""
def test_bot_host():
    test_bot_data = {
        "project_id":1,
        "version_id":1,
    }
    test_bot_response = {
        "host_id": os.getenv('BOTPRESS_ENDPOINT'),
        "bot_id": os.getenv('BOT_ID')
    }
    for url in urls:
        base_url = url  + "/api/v2/get-bot-host"
        r = requests.get(base_url,
            data=json.dumps(test_bot_data))
        data = r.json()

        assert data == test_bot_response, \
            "test bot link failed for " + url

"""
Basic conversation test
"""
def test_qna():
    inp = [
        {'query': 'can my daughter get immunised if she has a cold ?', 'user_id': '-1', 'trigger_search': True},
        {'query': 'booster', 'user_id': '768930bf736e05cc1c5609a91d9a7bff33493011c2576b7696a4ff4b676b079968d369178ea55c52c9c2f23ff87ed10ba0923c5fb63583d76aa605d826c2306b'},
        {'query': 'rubella', 'user_id': '768930bf736e05cc1c5609a91d9a7bff33493011c2576b7696a4ff4b676b079968d369178ea55c52c9c2f23ff87ed10ba0923c5fb63583d76aa605d826c2306b'},
        {'query': 'She is 6 years old', 'user_id': '768930bf736e05cc1c5609a91d9a7bff33493011c2576b7696a4ff4b676b079968d369178ea55c52c9c2f23ff87ed10ba0923c5fb63583d76aa605d826c2306b'}
    ]
    for url in urls:
        past_id = '-1'
        for x in inp:
            base_url = url  + '/api/v2/qna'
            if x['user_id'] == '-1':
                # pdb.set_trace()

                resp = requests.get(base_url, data=json.dumps(x)).json()
                past_id = resp['user_id']
            else:
                x['user_id']=past_id
                resp = requests.get(base_url, data=json.dumps(x)).json()

                if x['query']=='She is 6 years old':
                    assert resp['what_to_say']['question_0_variation_0']=='Is it possible to only get the measles vaccine without the mumps, rubella and varicella portion for a 6 year old? He has had very bad reactions to other vaccines.'

# def test_conversation():
#     for url in urls:
#         base_url= url + "/api/v2/qna"
#         data = [
#             [
#                 ("I need help","What topic is this most"),
#                 ("please help me", "What vaccine are you"),
#                 ("I am lost","For whom is this question"),
#                 ("save me !!!","Is there any additional information you"),
#                 ("none","Hi, I need to get a copy of my child record of immunization I hope the response answers your questions"),
#                 ("No","Would you like to ask another question"),
#                 ("No","I hope i was helpful"),
#             ],
#         ]
#         for snippet in data:
#             idx = 0
#             user_id = -1
#             for prompt, response in snippet:
#                 request = {
#                     "query":prompt,
#                     "user_id":user_id
#                 }   
#                 r = requests.get(base_url, data=json.dumps(request))
#                 data = r.json()
#                 print(data)
#                 pdb.set_trace()

# test_conversation()
        
# """
# QUESTION ASKER TIMING TEST
# """

# base_url= url + "/api/v2/qna"

# data_ = [
#     {
#         "query":"My child was vaccinated recently with MMR for school", 
#         "user_id":"-1"
#     }
#     ,
#     {
#         "query":"what restrictions are there for immuno compromised people visiting ?",
#         "user_id":"2d07dcffc217bf2864ba64fc8b60fdaa41d0b08f74fb522582f1031e77cb2a4fc3b5b0b98392efc0dce2b96f9be453c07373bfecea25964379c422e4f9e89877"
#     }
# ]

# times = []
# for x in range(1):
#     for idx,x in enumerate(data_):
#         if idx==1:
#             start = timeit.default_timer()
#         r = requests.get(base_url, data=json.dumps(x))
#         if idx==1:
#             stop = timeit.default_timer()
#             times.append(stop-start)
# print(mean(times))
# print(r.text)

# # """
# # Reranking timer test
# # """
# # base_url="http://18.203.115.216:5007/api/v1/reranking"

# # gpu_times_dict = {}
# # dir_ = "./accuracy_tests/intermediate_results"
# # for x in sorted(os.listdir(dir_)):
# #     title = os.path.join(dir_ , x)
# #     if not(title.endswith(".p")):
# #         continue

# #     batch_size = int(x.split("_")[2])
    
# #     if batch_size != 50:
# #         continue

# #     print("batch size : ", batch_size)


# #     gpu_times = []

# #     with open(title,'rb') as f:
# #         rerank_test = pickle.load(f)

# #     idx = 0
# #     accuracy = 0
# #     total = 0
# #     for x in rerank_test:
# #         idx += 1
# #         query_string = x[0]
# #         master_question = x[1]
# #         hits = x[2]
        

# #         texts = [[0,x[1]] for x in hits]


# #         start = timeit.default_timer()
# #         params = {
# #             "query": query_string,
# #             "texts": texts,
# #         }
# #         r = requests.get(base_url, json=json.dumps(params))
# #         response  = r.json()
# #         scoreDocs = response['scoreDocs']

# #         stop = timeit.default_timer()
# #         gpu_times.append(stop-start)
	
# # 	      #Top 5
# #         selected = scoreDocs[:5]
# #         for y in selected:
# #             if master_question == y[1]:
# #                 accuracy +=1
# #                 break
# #         total += 1


# #         if idx%10==0:
# #             print("mean time : ", mean(gpu_times))

# #         if idx%30== 0:
# #             print("mean time : ", mean(gpu_times[-30:]))
# #             break
# #     print(accuracy, total, accuracy/total)


# # print('$'*80)
# # print("reranking service done")


# # """
# # QUESTION ASKER TIMING TEST
# # """

# # base_url= url + "/api/v2/qna"

# # data_ = [
# #     {
# #         "query":"My child was vaccinated recently with MMR for school", 
# #         "user_id":"-1"
# #     }
# #     ,
# #     {
# #         "query":"what restrictions are there for \n immuno compromised people visiting ?",
# #         "user_id":"2d07dcffc217bf2864ba64fc8b60fdaa41d0b08f74fb522582f1031e77cb2a4fc3b5b0b98392efc0dce2b96f9be453c07373bfecea25964379c422e4f9e89877"
# #     }
# #     ,
# #     {
# #         "query":"none",
# #         "user_id":"2d07dcffc217bf2864ba64fc8b60fdaa41d0b08f74fb522582f1031e77cb2a4fc3b5b0b98392efc0dce2b96f9be453c07373bfecea25964379c422e4f9e89877"
# #     },
# #      {
# #         "query":"none",
# #         "user_id":"2d07dcffc217bf2864ba64fc8b60fdaa41d0b08f74fb522582f1031e77cb2a4fc3b5b0b98392efc0dce2b96f9be453c07373bfecea25964379c422e4f9e89877"
# #     }
# # ]

# # times = []
# # for x in range(1):
# #     for idx,x in enumerate(data_):
# #         if idx==1:
# #             start = timeit.default_timer()
# #         r = requests.get(base_url, data=json.dumps(x))
# #         if idx==1:
# #             stop = timeit.default_timer()
# #             times.append(stop-start)
# #         print(r.text)
# # print(mean(times))