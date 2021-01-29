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


f = open('/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/test_data/vla_data/answers.json',)
answer = json.load(f)
f.close()

answer_dict = {}
for x in answer:
    answer_dict[x['pk']]=x['text']

for x in os.listdir("./test_data/vla_data"):
    if x.endswith(".json"):
        path = os.path.join("./test_data/vla_data",x)
        if "questions" in x:
            pk = int(x.split('_')[3].strip(".json"))

            q = open(path,)
            questions = json.load(q)
            q.close()

            for x in  questions.keys():
                key = x

            
            for question in questions[key]:
                new_obj = {}
                question_statement = question[0]['value']

                new_obj['question']=question_statement
                new_obj['answer']=answer_dict[pk]
                new_obj['type']=key

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

            

# pdb.set_trace()

# xl = pd.read_csv("./vsn_data.csv")
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

# for idx,x in xl.iterrows():
#     object_dict = dict(x)
#     json_name = hashlib.sha512(x['question'].encode()).hexdigest()
#     json_file_name = "./test_data/vsn_data/" + json_name+".json"
#     with open(json_file_name , 'w') as json_file:
#         json.dump(object_dict, json_file, indent = 4, sort_keys=True)

# json_file_name = "./unique_keywords.json"
# with open(json_file_name , 'w') as json_file:
#     json.dump(config_dict, json_file, indent = 4, sort_keys=True)