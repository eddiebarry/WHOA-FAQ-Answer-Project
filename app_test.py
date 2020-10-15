import requests
import hashlib
import json

# """
# Single Keyword Extract Test
# """
# base_url="http://0.0.0.0:5006/api/v2/keyword_extract"
# params = {
#     "question":"My child is sick where can he get measles vaccine ?",
#     "answer":"Please go to khandala",
# }

# r = requests.get(base_url, params=params)
# print(r.text)
# """
# {
#     "Disease 1": [
#         "measles"
#     ], 
#     "Disease 2": [
#         "measles"
#     ], 
#     "Keyword": [
#         "child", 
#         "measles"
#     ], 
#     "Other -condition, symptom etc": [
#         "sick", 
#         "child"
#     ], 
#     "Subject - Person": [
#         "child"
#     ], 
#     "Vaccine 1": [
#         "measles"
#     ], 
#     "Vaccine 2": [
#         "measles"
#     ], 
#     "Who is writing this": [
#         "child"
#     ]
# }
# """


# """
# Batch Keyword Extract Test
# """
# qa_list = [
#     {
#         "question":"My child is sick where can he get measles vaccine ?",
#         "answer":"Please go to khandala",
#     },
#     {
#         "question":"My child is sick where can he get rubella vaccine ?",
#         "answer":"Please go to khandala",
#     },
#     {
#         "question":"My child is sick where can he get polio vaccine ?",
#         "answer":"Please go to khandala",
#     },
# ]

# for x in qa_list:
#     query_string = x['question']+x['answer']
#     qa_hash = hashlib.sha512(query_string.encode()).hexdigest()
#     x['hash']=qa_hash

# batch_response_test = {
#     "num_questions" : len(qa_list),
#     "question_answer_list" : qa_list
# }
# # print(json.dumps(batch_response_test,indent=4))
# """
# example input
# {
#     "num_questions": 3,
#     "question_answer_list": [
#         {
#             "question": "My child is sick where can he get measles vaccine ?",
#             "answer": "Please go to khandala",
#             "hash": "30f05b0d8b1d20dde20fd58ac8bc07e9ae1e664eefeada3d843d48dbe653afec1df8116a1755fb4a956166ecd67c61103f9fea5a9deb14ed1b551e80eecaeb5b"
#         },
#         {
#             "question": "My child is sick where can he get rubella vaccine ?",
#             "answer": "Please go to khandala",
#             "hash": "74ef7552dbf54d910a22174b0905b5965be9d2644cbb4d68406c9a23d128d20df8f6386106e8a7fdd7dddec549a204a54089887e89d0a86bf7cfca1ab2ba0ad8"
#         },
#         {
#             "question": "My child is sick where can he get polio vaccine ?",
#             "answer": "Please go to khandala",
#             "hash": "3b454a1b958d0abe190821768e21a837be283e02ff2c6a2b30d2f5363c1275221aabb35aa23319fc0ae24a33f022f8664b5a93d5eb0659c2eb1e1b0a2ae66383"
#         }
#     ]
# }
# """

# base_url="http://0.0.0.0:5006/api/v2/batch_keyword_extract"

# r = requests.get(base_url, data=json.dumps(batch_response_test))
# print(r.text)

# """
# {
#   "questions_keywords_dict": {
#     "30f05b0d8b1d20dde20fd58ac8bc07e9ae1e664eefeada3d843d48dbe653afec1df8116a1755fb4a956166ecd67c61103f9fea5a9deb14ed1b551e80eecaeb5b": {
#       "Disease 1": [
#         "measles"
#       ], 
#       "Disease 2": [
#         "measles"
#       ], 
#       "Keyword": [
#         "child", 
#         "measles", 
#         "immunize", 
#         "immunization"
#       ], 
#       "Other -condition, symptom etc": [
#         "sick", 
#         "child", 
#         "baby"
#       ], 
#       "Subject - Person": [
#         "child", 
#         "baby"
#       ], 
#       "Subject 1 - Immunization": [
#         "immunization", 
#         "vaccination"
#       ], 
#       "Subject 2 - Vaccination / General": [
#         "travel", 
#         "vaccination"
#       ], 
#       "Vaccine 1": [
#         "measles"
#       ], 
#       "Vaccine 2": [
#         "measles"
#       ], 
#       "Who is writing this": [
#         "child"
#       ]
#     }, 
#     "3b454a1b958d0abe190821768e21a837be283e02ff2c6a2b30d2f5363c1275221aabb35aa23319fc0ae24a33f022f8664b5a93d5eb0659c2eb1e1b0a2ae66383": {
#       "Disease 2": [
#         "polio"
#       ], 
#       "Keyword": [
#         "child", 
#         "immunize", 
#         "immunization"
#       ], 
#       "Other -condition, symptom etc": [
#         "sick", 
#         "child", 
#         "baby"
#       ], 
#       "Subject - Person": [
#         "child", 
#         "baby"
#       ], 
#       "Subject 1 - Immunization": [
#         "immunization", 
#         "vaccination"
#       ], 
#       "Subject 2 - Vaccination / General": [
#         "travel", 
#         "vaccination"
#       ], 
#       "Vaccine 1": [
#         "polio"
#       ], 
#       "Vaccine 2": [
#         "polio"
#       ], 
#       "Who is writing this": [
#         "child"
#       ]
#     }, 
#     "74ef7552dbf54d910a22174b0905b5965be9d2644cbb4d68406c9a23d128d20df8f6386106e8a7fdd7dddec549a204a54089887e89d0a86bf7cfca1ab2ba0ad8": {
#       "Disease 1": [
#         "rubella"
#       ], 
#       "Disease 2": [
#         "rubella"
#       ], 
#       "Keyword": [
#         "child", 
#         "immunize", 
#         "immunization"
#       ], 
#       "Other -condition, symptom etc": [
#         "sick", 
#         "child", 
#         "baby"
#       ], 
#       "Subject - Person": [
#         "child", 
#         "baby"
#       ], 
#       "Subject 1 - Immunization": [
#         "immunization", 
#         "vaccination"
#       ], 
#       "Subject 2 - Vaccination / General": [
#         "travel", 
#         "vaccination"
#       ], 
#       "Vaccine 1": [
#         "rubella"
#       ], 
#       "Vaccine 2": [
#         "rubella"
#       ], 
#       "Who is writing this": [
#         "child"
#       ]
#     }
#   }
# }
# """


"""
Batch QA index 
"""

data={
    "version_hash" : "user_1_version_1",
  }

import pandas as pd

xl = pd.read_excel("./tests/vsn_data.xlsx")
xl = xl.fillna("")
print(xl.head())