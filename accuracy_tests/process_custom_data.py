import pandas as pd
import json
import hashlib
import re
import os
import pdb

"""
This file processes the data given by the vaccine team into json objects that 
we can add to the search index
"""


# f = open('/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/test_data/vla_data/answers.json',)
# answer = json.load(f)
# f.close()

# answer_dict = {}
# for x in answer:
#     answer_dict[x['pk']]=x['text']

# for x in os.listdir("./test_data/vla_data"):
#     if x.endswith(".json"):
#         path = os.path.join("./test_data/vla_data",x)
#         if "questions" in x:
#             pk = int(x.split('_')[3].strip(".json"))

#             q = open(path,)
#             questions = json.load(q)
#             q.close()

#             for x in  questions.keys():
#                 key = x
questions = {
    0:"what can you do ?",
    1:"how can you help me ?",
    2:"what are your features ?",
}

answer_dict = {
    0:" I can help you with info regarding : \nHow to navigate through the course section\n How to edit your profile details\nInformation about your upcoming events",
    1:" I can help you with info regarding : \nHow to navigate through the course section\n How to edit your profile details\nInformation about your upcoming events",
    2:" I can help you with info regarding : \nHow to navigate through the course section\n How to edit your profile details\nInformation about your upcoming events",
}
            
for key in questions.keys():
    new_obj = {}
    question_statement = questions[key]

    new_obj['question']=question_statement
    new_obj['answer']=answer_dict[key]
    new_obj['type']="learning"

    json_file_name = hashlib.sha512(
            new_obj['question'].encode()
        ).hexdigest()

    json_file_name = os.path.join(
            "./intermediate_results/vla_data_no_variations",
            json_file_name+'.json'
        )
    print("writing", json_file_name)
    with open(json_file_name , 'w') as json_file:
        json.dump(new_obj, json_file,\
            indent = 4, sort_keys=True)

# create formatted data
for key in questions.keys():
    new_obj = {}
    question_statement = questions[key]

    new_obj['question']=question_statement
    new_obj['question_variation_0']=question_statement
    new_obj['question_variation_1']=question_statement
    new_obj['question_variation_2']=question_statement
    new_obj['answer']=answer_dict[key]
    new_obj['answer_formatted']=answer_dict[key]
    new_obj['type']="learning"

    json_file_name = hashlib.sha512(
            new_obj['question'].encode()
        ).hexdigest()

    json_file_name = os.path.join(
            "./intermediate_results/vla_data_formatted",
            json_file_name+'.json'
        )
    print("writing", json_file_name)
    with open(json_file_name , 'w') as json_file:
        json.dump(new_obj, json_file,\
            indent = 4, sort_keys=True)