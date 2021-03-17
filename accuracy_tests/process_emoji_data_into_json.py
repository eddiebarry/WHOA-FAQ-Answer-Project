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

            
#             for question in questions[key]:
#                 new_obj = {}
#                 question_statement = question[0]['value']

#                 new_obj['question']=question_statement
#                 new_obj['answer']=answer_dict[pk]
#                 new_obj['type']=key

#                 json_file_name = hashlib.sha512(
#                         new_obj['question'].encode()
#                     ).hexdigest()

#                 json_file_name = os.path.join(
#                         "./intermediate_results/vla_data_no_variations",
#                         json_file_name+'.json'
#                     )
#                 print("writing", json_file_name)
#                 with open(json_file_name , 'w') as json_file:
#                     json.dump(new_obj, json_file,\
#                         indent = 4, sort_keys=True)

#             # create formatted data
#             for question in questions[key]:
#                 new_obj = {}
#                 question_statement = question[0]['value']

#                 new_obj['question']=question_statement
#                 new_obj['question_variation_0']=question_statement
#                 new_obj['question_variation_1']=question_statement
#                 new_obj['question_variation_2']=question_statement
#                 new_obj['answer']=answer_dict[pk]
#                 new_obj['answer_formatted']=answer_dict[pk]
#                 new_obj['type']=key

#                 json_file_name = hashlib.sha512(
#                         new_obj['question'].encode()
#                     ).hexdigest()

#                 json_file_name = os.path.join(
#                         "./intermediate_results/vla_data_formatted",
#                         json_file_name+'.json'
#                     )
#                 print("writing", json_file_name)
#                 with open(json_file_name , 'w') as json_file:
#                     json.dump(new_obj, json_file,\
#                         indent = 4, sort_keys=True)

            

# pdb.set_trace()

xl = pd.read_csv("/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/emoji_qa.csv")

# xl = xl.fillna("")
# print(xl.head())

# config_dict = {}
# for x in xl.columns:
#     if x in ["question", "answer"]:
#         continue
#     config_dict[x]= list(xl[x].unique())

# def process_config_dict(dic):
#     new_dict = {}
#     for x in dic:
#         new_list = []
#         for string in dic[x]:
#             string = string.replace('(',',').replace(')',',').replace('/',',')\
#                 .replace("-"," ").replace("+",",")
#             new_ = string.lower().split(',')
#             new = [x.strip() for x in new_]
#             new_list.extend(new)
        
#         new_list = list(set(new_list))

#         if "" in new_list:
#             new_list.remove("")

#         new_dict[x] = new_list
    
#     return new_dict

# config_dict = process_config_dict(config_dict)

def return_type(string):
    pos_type = ["agenda","learning","course discovery","profile"]
    type_detected = ""
    for x in pos_type:
        if x in string:
            type_detected += " " + x
    
    return type_detected.strip()

for idx,x in xl.iterrows():
    object_dict = dict(x)
    # print(x['Question'])
    # print(x['Edited Answer'])

    # break
    for question in x['Question'].split('/'):
        # pdb.set_trace()
        if type(x['Edited Answer']) != str:
            break

        question = question.strip()
        object_dict = {
            "answer": x['Edited Answer'],
            "answer_formatted": x['Edited Answer'],
            "question": question,
            "question_variation_0": question,
            "question_variation_1": question,
            "question_variation_2": question,
        }
        
        # try:
        object_dict['type'] = return_type(question + " " + x['Edited Answer'])
        # except:
        #     pdb.set_trace()

        json_name = hashlib.sha512(x['Question'].encode()).hexdigest()
        json_file_name = "./accuracy_tests/intermediate_results/emoji_data_formatted/" + json_name+".json"
        with open(json_file_name , 'w') as json_file:
            json.dump(object_dict, json_file, indent = 4, sort_keys=True)
            break

# json_file_name = "./unique_keywords.json"
# with open(json_file_name , 'w') as json_file:
#     json.dump(config_dict, json_file, indent = 4, sort_keys=True)