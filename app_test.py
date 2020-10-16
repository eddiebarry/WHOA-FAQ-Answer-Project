import requests
import hashlib
import json
import os
import pickle
import timeit
from statistics import mean 
# TODO : Use Pytest

"""
Single Keyword Extract Test
"""
base_url="http://0.0.0.0:5007/api/v2/keyword_extract"
params = {
    "question":"My child is sick where can he get measles vaccine ?",
    "answer":"Please go to khandala",
}

r = requests.get(base_url, params=params)
print(r.text)
"""
{
    "Disease 1": [
        "measles"
    ], 
    "Disease 2": [
        "measles"
    ], 
    "Keyword": [
        "child", 
        "measles"
    ], 
    "Other -condition, symptom etc": [
        "sick", 
        "child"
    ], 
    "Subject - Person": [
        "child"
    ], 
    "Vaccine 1": [
        "measles"
    ], 
    "Vaccine 2": [
        "measles"
    ], 
    "Who is writing this": [
        "child"
    ]
}
"""


"""
Batch Keyword Extract Test
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
    x['hash']=qa_hash

batch_response_test = {
    "num_questions" : len(qa_list),
    "question_answer_list" : qa_list
}
# print(json.dumps(batch_response_test,indent=4))
"""
example input
{
    "num_questions": 3,
    "question_answer_list": [
        {
            "question": "My child is sick where can he get measles vaccine ?",
            "answer": "Please go to khandala",
            "hash": "30f05b0d8b1d20dde20fd58ac8bc07e9ae1e664eefeada3d843d48dbe653afec1df8116a1755fb4a956166ecd67c61103f9fea5a9deb14ed1b551e80eecaeb5b"
        },
        {
            "question": "My child is sick where can he get rubella vaccine ?",
            "answer": "Please go to khandala",
            "hash": "74ef7552dbf54d910a22174b0905b5965be9d2644cbb4d68406c9a23d128d20df8f6386106e8a7fdd7dddec549a204a54089887e89d0a86bf7cfca1ab2ba0ad8"
        },
        {
            "question": "My child is sick where can he get polio vaccine ?",
            "answer": "Please go to khandala",
            "hash": "3b454a1b958d0abe190821768e21a837be283e02ff2c6a2b30d2f5363c1275221aabb35aa23319fc0ae24a33f022f8664b5a93d5eb0659c2eb1e1b0a2ae66383"
        }
    ]
}
"""

base_url="http://0.0.0.0:5007/api/v2/batch_keyword_extract"

r = requests.get(base_url, data=json.dumps(batch_response_test))
print(r.text)

"""
{
  "questions_keywords_dict": {
    "30f05b0d8b1d20dde20fd58ac8bc07e9ae1e664eefeada3d843d48dbe653afec1df8116a1755fb4a956166ecd67c61103f9fea5a9deb14ed1b551e80eecaeb5b": {
      "Disease 1": [
        "measles"
      ], 
      "Disease 2": [
        "measles"
      ], 
      "Keyword": [
        "child", 
        "measles", 
        "immunize", 
        "immunization"
      ], 
      "Other -condition, symptom etc": [
        "sick", 
        "child", 
        "baby"
      ], 
      "Subject - Person": [
        "child", 
        "baby"
      ], 
      "Subject 1 - Immunization": [
        "immunization", 
        "vaccination"
      ], 
      "Subject 2 - Vaccination / General": [
        "travel", 
        "vaccination"
      ], 
      "Vaccine 1": [
        "measles"
      ], 
      "Vaccine 2": [
        "measles"
      ], 
      "Who is writing this": [
        "child"
      ]
    }, 
    "3b454a1b958d0abe190821768e21a837be283e02ff2c6a2b30d2f5363c1275221aabb35aa23319fc0ae24a33f022f8664b5a93d5eb0659c2eb1e1b0a2ae66383": {
      "Disease 2": [
        "polio"
      ], 
      "Keyword": [
        "child", 
        "immunize", 
        "immunization"
      ], 
      "Other -condition, symptom etc": [
        "sick", 
        "child", 
        "baby"
      ], 
      "Subject - Person": [
        "child", 
        "baby"
      ], 
      "Subject 1 - Immunization": [
        "immunization", 
        "vaccination"
      ], 
      "Subject 2 - Vaccination / General": [
        "travel", 
        "vaccination"
      ], 
      "Vaccine 1": [
        "polio"
      ], 
      "Vaccine 2": [
        "polio"
      ], 
      "Who is writing this": [
        "child"
      ]
    }, 
    "74ef7552dbf54d910a22174b0905b5965be9d2644cbb4d68406c9a23d128d20df8f6386106e8a7fdd7dddec549a204a54089887e89d0a86bf7cfca1ab2ba0ad8": {
      "Disease 1": [
        "rubella"
      ], 
      "Disease 2": [
        "rubella"
      ], 
      "Keyword": [
        "child", 
        "immunize", 
        "immunization"
      ], 
      "Other -condition, symptom etc": [
        "sick", 
        "child", 
        "baby"
      ], 
      "Subject - Person": [
        "child", 
        "baby"
      ], 
      "Subject 1 - Immunization": [
        "immunization", 
        "vaccination"
      ], 
      "Subject 2 - Vaccination / General": [
        "travel", 
        "vaccination"
      ], 
      "Vaccine 1": [
        "rubella"
      ], 
      "Vaccine 2": [
        "rubella"
      ], 
      "Who is writing this": [
        "child"
      ]
    }
  }
}
"""


"""
Batch QA index 
"""

data = {
  "version_hash" : "user_1_version_1",
}
questions = []
dir_ = "./tests/test_data/vsn_data"
dir_ = "./tests/intermediate_results/vsn_data_variations"
for idx,x in enumerate(sorted(os.listdir(dir_))):
	if x.endswith(".json"):
		jsonpath = os.path.join(dir_,x)
		f = open(jsonpath,)
		jsonObj = json.load(f)
		jsonObj['id']=str(idx)
		f.close()
		questions.append(jsonObj)

keyword_dir_path = "./tests/unique_keywords.json"
f = open(keyword_dir_path,)
keyword_directory = json.load(f)

data['question_array'] = questions
data['keyword_directory'] = keyword_directory

base_url="http://0.0.0.0:5007/api/v2/train_bot_json_array"

r = requests.post(base_url, data=json.dumps(data))
print(r.text)

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


base_url="http://0.0.0.0:5007/api/v2/qna"

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
print(r.text)