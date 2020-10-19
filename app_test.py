import requests
import hashlib
import json
import os
import pickle
import timeit
from statistics import mean 
# TODO : Use Pytest


# url = "http://52.209.188.140:5007"
url = "http://0.0.0.0:5007"

"""
Batch Keyword Extract Test

example input
{
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

example response
{
  "questions_keywords_list": [
    {
      "id": "1"
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
          "i", 
          "immunization"
        ], 
        "subject_2_vaccination_general": [
          "vaccination", 
          "travel"
        ], 
        "subject_person": [
          "baby", 
          "child"
        ], 
        "vaccine_1": [
          "measles"
        ], 
        "vaccine_2": [
          "measles"
        ], 
        "who_is_writing_this": [
          "child"
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
          "i", 
          "immunization"
        ], 
        "subject_2_vaccination_general": [
          "vaccination", 
          "travel"
        ], 
        "subject_person": [
          "baby", 
          "child"
        ], 
        "vaccine_1": [
          "rubella"
        ], 
        "vaccine_2": [
          "rubella"
        ], 
        "who_is_writing_this": [
          "child"
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
          "i", 
          "immunization"
        ], 
        "subject_2_vaccination_general": [
          "vaccination", 
          "travel"
        ], 
        "subject_person": [
          "baby", 
          "child"
        ], 
        "vaccine_1": [
          "polio"
        ], 
        "vaccine_2": [
          "polio"
        ], 
        "who_is_writing_this": [
          "child"
        ]
      }
    }
  ]
}
"""
qa_list = [
    {
        "question":"My child is sick where can he get measles vaccine ?",
        "answer":"Please go to khandala",
    },
    {
        "question":"My child is sick where can he get rubella vaccine ?",
        "answer":"Please go to khandala",
    },
    {
        "question":"My child is sick where can he get polio vaccine ?",
        "answer":"Please go to khandala",
    },
]

for x in qa_list:
    query_string = x['question']+x['answer']
    qa_hash = hashlib.sha512(query_string.encode()).hexdigest()
    x['id']=qa_hash

batch_response_test = {
    "question_answer_list" : qa_list
}

base_url = url  + "/api/v2/batch_keyword_extract"
r = requests.post(base_url, data=json.dumps(batch_response_test))
print(json.dumps(batch_response_test,indent=4))
print(r.text)


"""
Batch QA index 

example input
{
    "project_id":"1",
    "version_id":"0.1",
    "version_number":"0.1",
    "question_list" : [
        {
            "question" : "where can i get a vaccine in khandala",
            "answer" : "go to hospital",
            "keywords" : [
                {
                    "category_1" : [
                    "cat_1_key_1",
                    "cat_1_key_2",
                    ]
                },
                {
                    "category_2" : [
                    "cat_2_key_1",
                    "cat_2_key_2",
                    ]
                }
            ],
            "id": "12345"
        },
        {
            "question" : "where can i get a vaccine in lonavla",
            "answer" : "go to hospital",
            "keywords" : [
                {
                    "category_1" : [
                    "cat_1_key_1",
                    "cat_1_key_2",
                    ]
                },
                {
                    "category_2" : [
                    "cat_2_key_1",
                    "cat_2_key_2",
                    ]
                }
            ],
            "id": "23456"
        },
        # case where no keyword in a category
        {
            "question" : "where can i get a vaccine in san marino",
            "answer" : "go to hospital",
            "keywords" : [],
            "id" : "34567"
        }
    ],
    "keyword_directory" : [
        {"category_1" : ["cat_1_keyword_1", "cat_1_keyword_2"]},
        {"category_2" : ["cat_2_keyword_1", "cat_1_keyword_2"]}
    ]
}

example output :
{
  "project_id": "1", 
  "status": "ok", 
  "version_id": "0.1"
}
"""

data = {
    "project_id":"1",
    "version_id":"0.1",
    "version_number":"0.1",
    "question_list" : [
        {
            "question" : "where can i get a vaccine in khandala",
            "answer" : "go to hospital",
            "keywords" : [
                {
                    "category_1" : [
                    "cat_1_key_1",
                    "cat_1_key_2",
                    ]
                },
                {
                    "category_2" : [
                    "cat_2_key_1",
                    "cat_2_key_2",
                    ]
                }
            ],
            "id": "12345"
        },
        {
            "question" : "where can i get a vaccine in lonavla",
            "answer" : "go to hospital",
            "keywords" : [
                {
                    "category_1" : [
                    "cat_1_key_1",
                    "cat_1_key_2",
                    ]
                },
                {
                    "category_2" : [
                    "cat_2_key_1",
                    "cat_2_key_2",
                    ]
                }
            ],
            "id": "23456"
        },
        # case where no keyword in a category
        {
            "question" : "where can i get a vaccine in san marino",
            "answer" : "go to hospital",
            "keywords" : [],
            "id" : "34567"
        }
    ],
    "keyword_directory" : [
        {"category_1" : ["cat_1_keyword_1", "cat_1_keyword_2"]},
        {"category_2" : ["cat_2_keyword_1", "cat_1_keyword_2"]}
    ]
}
base_url= url + "/api/v2/train_bot_json_array"

r = requests.post(base_url, data=json.dumps(data))
print(r.text)

data = {
    "project_id":"1",
    "version_id":"0.3",
    "version_number":"0.1",
}
questions = []
# dir_ = "./tests/test_data/vsn_data"
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
data['keyword_directory'] = keyword_directory

base_url= url + "/api/v2/train_bot_json_array"

r = requests.post(base_url, data=json.dumps(data))
print(r.text)


"""
Reranking timer test
"""
base_url="http://18.203.115.216:5007/api/v1/reranking"

gpu_times_dict = {}
dir_ = "./tests/intermediate_results"
for x in sorted(os.listdir(dir_)):
    title = os.path.join(dir_ , x)
    if not(title.endswith(".p")):
        continue

    batch_size = int(x.split("_")[2])
    
    if batch_size != 50:
        continue

    print("batch size : ", batch_size)


    gpu_times = []

    with open(title,'rb') as f:
        rerank_test = pickle.load(f)

    idx = 0
    accuracy = 0
    total = 0
    for x in rerank_test:
        idx += 1
        query_string = x[0]
        master_question = x[1]
        hits = x[2]
        

        texts = [[0,x[1]] for x in hits]


        start = timeit.default_timer()
        params = {
            "query": query_string,
            "texts": texts,
        }
        r = requests.get(base_url, json=json.dumps(params))
        response  = r.json()
        scoreDocs = response['scoreDocs']

        stop = timeit.default_timer()
        gpu_times.append(stop-start)
	
	      #Top 5
        selected = scoreDocs[:5]
        for y in selected:
            if master_question == y[1]:
                accuracy +=1
                break
        total += 1


        if idx%10==0:
            print("mean time : ", mean(gpu_times))

        if idx%30== 0:
            print("mean time : ", mean(gpu_times[-30:]))
            break
    print(accuracy, total, accuracy/total)


print('$'*80)
print("reranking service done")


"""
QUESTION ASKER TIMING TEST
"""

base_url= url + "/api/v2/qna"

data_ = [
    {
        "query":"My child was vaccinated recently with MMR for school", 
        "user_id":"-1"
    }
    ,
    {
        "query":"what restrictions are there for immuno compromised people visiting ?",
        "user_id":"2d07dcffc217bf2864ba64fc8b60fdaa41d0b08f74fb522582f1031e77cb2a4fc3b5b0b98392efc0dce2b96f9be453c07373bfecea25964379c422e4f9e89877"
    }
]

times = []
for x in range(30):
    for idx,x in enumerate(data_):
        if idx==1:
            start = timeit.default_timer()
        r = requests.get(base_url, data=json.dumps(x))
        if idx==1:
            stop = timeit.default_timer()
            times.append(stop-start)
print(mean(times))
# print(r.text)