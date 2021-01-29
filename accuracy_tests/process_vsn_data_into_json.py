import pandas as pd
import json
import hashlib
import re
import os

"""
This file processes the data given by the vaccine team into json objects that 
we can add to the search index
"""


xl = pd.read_csv("./vsn_data.csv")
xl = xl.fillna("")
print(xl.head())

config_dict = {}
for x in xl.columns:
    if x in ["question", "answer"]:
        continue
    config_dict[x]= list(xl[x].unique())

def process_config_dict(dic):
    new_dict = {}
    for x in dic:
        new_list = []
        for string in dic[x]:
            string = string.replace('(',',').replace(')',',').replace('/',',')\
                .replace("-"," ").replace("+",",")
            new_ = string.lower().split(',')
            new = [x.strip() for x in new_]
            new_list.extend(new)
        
        new_list = list(set(new_list))

        if "" in new_list:
            new_list.remove("")

        new_dict[x] = new_list
    
    return new_dict

config_dict = process_config_dict(config_dict)

for idx,x in xl.iterrows():
    object_dict = dict(x)
    json_name = hashlib.sha512(x['question'].encode()).hexdigest()
    json_file_name = "./test_data/vsn_data/" + json_name+".json"
    with open(json_file_name , 'w') as json_file:
        json.dump(object_dict, json_file, indent = 4, sort_keys=True)

json_file_name = "./unique_keywords.json"
with open(json_file_name , 'w') as json_file:
    json.dump(config_dict, json_file, indent = 4, sort_keys=True)