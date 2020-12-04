import requests
import hashlib
import json
import os
import pickle
import timeit
from statistics import mean 
import pdb


def populate_1500_questions(project_id=999, version_id=0, \
    previous_versions=[], url="http://52.209.188.140:5008",local=False):
    if local:
        url = "http://0.0.0.0:5008"
    data = {
        "project_id":project_id,
        "version_id":version_id,
        "previous_versions" : previous_versions
    }
    questions = []
    dir_ = "./tests/intermediate_results/vsn_data_variations"
    protected = [
            'question','answer','question_variation_0',
            'question_variation_1','question_variation_2', 'id'
        ]
    for idx,x in enumerate(sorted(os.listdir(dir_))):
        if x.endswith(".json"):
            jsonpath = os.path.join(dir_,x)
            f = open(jsonpath,)
            jsonObj = json.load(f)
            jsonObj['id']=str(idx)
            f.close()
            keywords = []
            to_remove = []
            for x in jsonObj.keys():
                if x in protected:
                    continue
                if jsonObj[x] != "":
                    new_dict = {
                        x: [jsonObj[x]]
                    }
                    keywords.append(new_dict)
                to_remove.append(x)
            for x in to_remove:    
                jsonObj.pop(x,None)
            jsonObj['keywords']=keywords
            questions.append(jsonObj)

    keyword_dir_path = "./tests/unique_keywords.json"
    f = open(keyword_dir_path,)
    keyword_directory = json.load(f)

    data['question_list'] = questions

    new_dir = []
    for x in keyword_directory:
        new_dir.append({x:keyword_directory[x]})
    data['keyword_directory'] = new_dir

    base_url= url + "/api/v2/train_bot_json_array"
    r = requests.post(base_url, data=json.dumps(data))
    print(r.text)
    print(len(questions), "is the number of questions added")